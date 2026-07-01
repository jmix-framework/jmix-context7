<Path>Add-ons > GroupDataGrid > GroupDataGrid with grouping by custom column</Path>

GroupDataGrid can group data items by non-persistent properties. To enable grouping, describe the property in the GroupDataGridItems. It requires a GroupPropertyDescriptor object where you can define the property name and its value provider. Note that the property name must match the column key that is not bound to an entity property. By default, sorting will not work for this property. To sort the data correctly, you can specify properties from an entity. For example, if you use BaseGroupPropertyDescriptor (the base implementation of GroupPropertyDescriptor), you can set sort properties using the withSortProperties() method. These properties will be used for sorting.

group-data-grid-custom-column.xml

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
            <groupg:columns>
                <groupg:groupColumn key="group" header="msg://customersGroupDataGrid.group.header" resizable="true"/>
                <groupg:column key="fullName" header="msg://customersGroupDataGrid.fullName.header"/>
                <groupg:column property="email"/>
                <groupg:column property="age"/>
                <groupg:column property="active"/>
            </groupg:columns>
        </groupg:groupDataGrid>
    </layout>
</view>




GroupDataGridCustomColumnSample.java

package io.jmix.uisamples.view.flowui.groupdatagrid.customcolumn;

import com.vaadin.flow.data.renderer.Renderer;
import com.vaadin.flow.data.renderer.TextRenderer;
import io.jmix.flowui.component.groupgrid.data.GroupDataGridItems;
import io.jmix.flowui.view.*;
import io.jmix.groupgridflowui.component.GroupDataGrid;
import io.jmix.groupgridflowui.data.BaseGroupPropertyDescriptor;
import io.jmix.uisamples.entity.Customer;

import java.util.List;

@ViewController("group-data-grid-custom-column")
@ViewDescriptor(value = "group-data-grid-custom-column.xml")
public class GroupDataGridCustomColumnSample extends StandardView {

    @ViewComponent
    private GroupDataGrid<Customer> customersGroupDataGrid;

    @Subscribe
    public void onInit(InitEvent event) {
        GroupDataGridItems<Customer> items = customersGroupDataGrid.getItems();

        if (items != null) {
            items.addGroupPropertyDescriptor(
                    new BaseGroupPropertyDescriptor<Customer>("fullName",
                            context -> context.getItem().getName() + " " + context.getItem().getLastName())
                            .withSortProperties(List.of("name", "lastName")));

            customersGroupDataGrid.groupByKeys("fullName");
        }
    }

    @Supply(to = "customersGroupDataGrid.fullName", subject = "renderer")
    protected Renderer<Customer> supplyRendererToFullNameColumn() {
        return new TextRenderer<>(item -> item.getName() + " " + item.getLastName());
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


