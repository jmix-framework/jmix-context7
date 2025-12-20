<Path>Add-ons > GroupDataGrid > GroupDataGrid with a component renderer for group column</Path>

To provide a custom component for a group row, use the GroupDataGridColumnComponentRenderer renderer. You can add a group column with custom column content using the addComponentGroupColumn() method.

group-data-grid-renderer.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:groupg="http://jmix.io/schema/groupgrid/ui">
    <data>
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_base">
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
    <layout>
        <groupg:groupDataGrid id="customersGroupDataGrid"
                              dataContainer="customersDc"
                              width="100%"
                              minHeight="20em">
            <groupg:groupBy>
                <groupg:columnRef key="grade"/>
            </groupg:groupBy>
            <groupg:columns>
                <groupg:groupColumn key="group" header="msg://customersGroupDataGrid.group.header" resizable="true"/>
                <groupg:column property="grade"/>
                <groupg:column property="name"/>
                <groupg:column property="lastName"/>
                <groupg:column property="email"/>
                <groupg:column property="age"/>
            </groupg:columns>
        </groupg:groupDataGrid>
    </layout>
</view>




GroupDataGridRendererSample.java

package io.jmix.uisamples.view.flowui.groupdatagrid.renderer;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.data.renderer.Renderer;
import io.jmix.core.MetadataTools;
import io.jmix.flowui.view.*;
import io.jmix.groupgridflowui.component.renderer.GroupDataGridColumnComponentRenderer;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.CustomerGrade;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("group-data-grid-renderer")
@ViewDescriptor(value = "group-data-grid-renderer.xml")
public class GroupDataGridRendererSample extends StandardView {

    @Autowired
    private MetadataTools metadataTools;

    @Supply(to = "customersGroupDataGrid.group", subject = "renderer")
    public Renderer<Customer> supplyRendererToGroupColumn() {
        return new GroupDataGridColumnComponentRenderer<>(groupInfo ->
                groupInfo.getProperty().is("grade")
                        ? createGradeLayout(groupInfo.getValue())
                        : new Span(metadataTools.format(groupInfo.getValue())));
    }

    protected Component createGradeLayout(CustomerGrade grade) {
        HorizontalLayout root = new HorizontalLayout();
        root.setPadding(false);
        root.add(new Span(metadataTools.format(grade)));

        Icon icon = VaadinIcon.DIAMOND.create();
        icon.getStyle().set("color", getGradeColor(grade));
        root.add(icon);
        return root;
    }

    private String getGradeColor(CustomerGrade grade) {
        return switch (grade) {
            case HIGH -> "#1F3A93";
            case PREMIUM -> "#AE0CAF";
            default -> "#D7D7D7";
        };
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
import org.springframework.lang.Nullable;

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
import org.springframework.lang.Nullable;

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


