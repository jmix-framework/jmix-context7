<Path>Layouts > GridLayout > GridLayout with custom renderer</Path>

To configure custom rendering of grid items, `renderer` is used. It can be set using the `setRenderer` method, or the
declarative `@Supply` construct in the view controller.

This sample demonstrates the `renderer` for the `Customer` entity card. The component also supports using [
`fragmentRenderer`]({contextPath}/sample/fragment-renderer).


grid-layout-renderer.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="customerDc" class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_base">
            <loader id="customerDl" readOnly="true">
                <query>
                    <![CDATA[select e from Customer e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <split width="100%" height="100%">
            <vbox>
                <gridLayout id="gridLayout" itemsContainer="customerDc" gap="var(--lumo-space-m)"
                            width="100%" height="100%"/>
            </vbox>
            <div/>
        </split>
    </layout>
</view>




GridLayoutRendererSample.java

package io.jmix.uisamples.view.flowui.containers.gridlayout.renderer;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.avatar.Avatar;
import com.vaadin.flow.component.badge.Badge;
import com.vaadin.flow.component.badge.BadgeVariant;
import com.vaadin.flow.component.card.CardVariant;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.data.renderer.ComponentRenderer;
import io.jmix.core.MessageTools;
import io.jmix.core.Metadata;
import io.jmix.core.MetadataTools;
import io.jmix.core.metamodel.model.MetaClass;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.card.JmixCard;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Supply;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.CustomerGrade;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Objects;

@ViewController("grid-layout-renderer")
@ViewDescriptor("grid-layout-renderer.xml")
public class GridLayoutRendererSample extends StandardView {

    @Autowired
    private UiComponents uiComponents;
    @Autowired
    private MetadataTools metadataTools;
    @Autowired
    private MessageTools messageTools;
    @Autowired
    private Metadata metadata;

    private int colorIndex;

    @Supply(to = "gridLayout", subject = "renderer")
    public ComponentRenderer<JmixCard, Customer> customerRenderer() {
        return new ComponentRenderer<>(this::createCard, this::initCard);
    }

    private JmixCard createCard() {
        JmixCard card = uiComponents.create(JmixCard.class);
        card.setWidthFull();
        card.addThemeVariants(CardVariant.OUTLINED, CardVariant.ELEVATED);
        return card;
    }

    private void initCard(JmixCard card, Customer customer) {
        card.setHeaderPrefix(createAvatar(customer));
        card.setTitle(customer.getInstanceName());
        card.setSubtitle(createSubtitle(customer));
        card.add(createAdditionalInfo(customer));
    }

    private Avatar createAvatar(Customer customer) {
        Avatar avatar = new Avatar(customer.getInstanceName());
        avatar.setColorIndex(colorIndex++ % 7);
        return avatar;
    }

    private Component createSubtitle(Customer customer) {
        Span span = uiComponents.create(Span.class);
        String ageCaption = getPropertyCaption(customer, "age");
        span.setText("%s: %s".formatted(ageCaption, customer.getAge()));
        return span;
    }

    private Component createAdditionalInfo(Customer customer) {
        HorizontalLayout emailLayout = uiComponents.create(HorizontalLayout.class);
        emailLayout.setPadding(false);
        emailLayout.add(createPropertyCaption(customer, "email"), new Span(customer.getEmail()));

        HorizontalLayout gradeLayout = uiComponents.create(HorizontalLayout.class);
        gradeLayout.setPadding(false);
        gradeLayout.add(createPropertyCaption(customer, "grade"), createGradeBadge(customer));

        VerticalLayout infoLayout = uiComponents.create(VerticalLayout.class);
        infoLayout.add(emailLayout, gradeLayout);
        return infoLayout;
    }

    private Component createPropertyCaption(Customer customer, String property) {
        Span span = uiComponents.create(Span.class);
        String propertyCaption = getPropertyCaption(customer, property);
        span.setText("%s: ".formatted(propertyCaption));
        return span;
    }

    private String getPropertyCaption(Customer customer, String property) {
        MetaClass metaClass = metadata.getClass(customer);
        return messageTools.getPropertyCaption(metaClass, property);
    }

    private Component createGradeBadge(Customer customer) {
        CustomerGrade gradeValue = Objects.requireNonNull(customer.getGrade());

        Badge badge = uiComponents.create(Badge.class);
        badge.setText(metadataTools.format(gradeValue));

        if (gradeValue == CustomerGrade.HIGH) {
            badge.addThemeVariants(BadgeVariant.SUCCESS);
        } else if (gradeValue == CustomerGrade.PREMIUM) {
            badge.addThemeVariants(BadgeVariant.FILLED);
        }

        return badge;
    }
}




Customer.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import org.jspecify.annotations.Nullable;

import java.util.UUID;

@Table(name = "CUSTOMER")
@Entity
@JmixEntity
public class Customer {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", length = 50, nullable = false)
    protected String name;

    @Column(name = "LAST_NAME", length = 100, nullable = false)
    protected String lastName;

    @Email
    @Column(name = "EMAIL", nullable = false)
    protected String email;

    @Column(name = "AGE")
    protected Integer age;

    @Column(name = "ACTIVE", nullable = false)
    protected Boolean active = false;

    @Column(name = "GRADE")
    protected Integer grade;

    public Boolean getActive() {
        return active;
    }

    public Customer() {
        this.id = UUID.randomUUID();
    }

    @InstanceName
    @DependsOnProperties({"name", "lastName"})
    public String getInstanceName() {
        return name + " " + lastName;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setGrade(@Nullable CustomerGrade grade) {
        this.grade = grade == null ? null : grade.getId();
    }

    @Nullable
    public CustomerGrade getGrade() {
        return grade == null ? null : CustomerGrade.fromId(grade);
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public Boolean isActive() {
        return active;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getAge() {
        return age;
    }
}




CustomerGrade.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.jspecify.annotations.Nullable;

public enum CustomerGrade implements EnumClass<Integer> {

    PREMIUM(10),
    HIGH(20),
    STANDARD(30);

    private final Integer id;

    CustomerGrade(Integer id) {
        this.id = id;
    }

    @Override
    public Integer getId() {
        return id;
    }

    @Nullable
    public static CustomerGrade fromId(Integer id) {
        for (CustomerGrade grade : CustomerGrade.values()) {
            if (grade.getId().equals(id))
                return grade;
        }
        return null;
    }
}


