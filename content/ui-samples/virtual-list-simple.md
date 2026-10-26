<Path>Components > VirtualList > Simple VirtualList</Path>

VirtualList allows you to render a long list of items inside a scrollable container without sacrificing performance. Each item is rendered on the fly as the user scrolls the list. A custom renderer for list items can be set in view controller using Java code only. It's possible to specify a renderer using ValueProvider if we want to show some plain text. You can use the setRenderer() method or @Supply annotation for it.

virtual-list-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer">
            <fetchPlan extends="_base"/>
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout alignItems="CENTER" classNames="virtual-list-simple">
        <virtualList id="virtualList" width="30em"
                     itemsContainer="customersDc"
                     alignSelf="CENTER"/>
    </layout>
</view>




VirtualListSimpleSample.java

package io.jmix.uisamples.view.flowui.components.virtuallist.simple;

import com.vaadin.flow.component.badge.Badge;
import com.vaadin.flow.component.badge.BadgeVariant;
import com.vaadin.flow.component.html.H4;
import com.vaadin.flow.component.html.H5;
import com.vaadin.flow.component.html.Hr;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.data.renderer.ComponentRenderer;
import com.vaadin.flow.data.renderer.Renderer;
import io.jmix.core.MetadataTools;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.details.JmixDetails;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Supply;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.CustomerGrade;
import org.jspecify.annotations.Nullable;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("virtual-list-simple")
@ViewDescriptor("virtual-list-simple.xml")
public class VirtualListSimpleSample extends StandardView {

    @Autowired
    protected UiComponents uiComponents;
    @Autowired
    protected MetadataTools metadataTools;

    @Supply(to = "virtualList", subject = "renderer")
    protected Renderer<Customer> virtualListRenderer() {
        return new ComponentRenderer<>(customer -> {
            VerticalLayout infoLayout = createVerticalLayout();
            infoLayout.addClassNames("info-layout");

            H4 customerName = new H4(customer.getInstanceName());
            Badge gradeBadge = createGradeBadge(customer.getGrade());
            infoLayout.add(customerName, gradeBadge);

            HorizontalLayout infoLine = createHorizontalLayout();
            infoLine.setAlignItems(FlexComponent.Alignment.CENTER);

            H5 emailLabel = new H5("Email:");
            Span email = new Span(customer.getEmail());
            infoLine.add(emailLabel, email);

            HorizontalLayout infoLine2 = createHorizontalLayout();

            H5 ageLabel = new H5("Age:");
            Span age = new Span(String.valueOf(customer.getAge()));

            infoLine2.add(ageLabel, age);

            VerticalLayout additionalInfoLayout = createVerticalLayout();
            additionalInfoLayout.add(infoLine, infoLine2);

            JmixDetails infoDetails = uiComponents.create(JmixDetails.class);
            infoDetails.setSummaryText("Additional information");
            infoDetails.add(additionalInfoLayout);

            infoLayout.add(infoDetails, new Hr());
            return infoLayout;
        });
    }

    protected VerticalLayout createVerticalLayout() {
        VerticalLayout layout = uiComponents.create(VerticalLayout.class);
        layout.setSpacing(false);
        layout.setPadding(false);
        return layout;
    }

    protected HorizontalLayout createHorizontalLayout() {
        HorizontalLayout layout = uiComponents.create(HorizontalLayout.class);
        layout.setPadding(false);
        return layout;
    }

    protected Badge createGradeBadge(@Nullable CustomerGrade grade) {
        Badge gradeBadge = new Badge(metadataTools.format(grade));

        if (grade == CustomerGrade.HIGH) {
            gradeBadge.addThemeVariants(BadgeVariant.SUCCESS);
        } else if (grade == CustomerGrade.PREMIUM) {
            gradeBadge.addThemeVariants(BadgeVariant.FILLED);
        }

        return gradeBadge;
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




virtual-list-simple.css


.virtual-list-simple .info-layout {
    padding-bottom: var(--vaadin-padding-s);
    padding-top: var(--vaadin-padding-s);
    gap: var(--vaadin-gap-s);
}


