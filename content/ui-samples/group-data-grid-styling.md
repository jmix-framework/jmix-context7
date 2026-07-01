<Path>Add-ons > GroupDataGrid > GroupDataGrid styling</Path>

To highlight a group row or group column cells, use the setGroupPartNameGenerator() method.

group-data-grid-styling.xml

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
                <groupg:column property="active"/>
            </groupg:columns>
        </groupg:groupDataGrid>
    </layout>
</view>




GroupDataGridStylingSample.java

package io.jmix.uisamples.view.flowui.groupdatagrid.styling;

import io.jmix.flowui.component.groupgrid.GroupInfo;
import io.jmix.flowui.component.groupgrid.GroupProperty;
import io.jmix.flowui.view.*;
import io.jmix.groupgridflowui.component.DataGridColumn;
import io.jmix.groupgridflowui.component.GroupDataGrid;
import io.jmix.uisamples.entity.Customer;

@ViewController("group-data-grid-styling")
@ViewDescriptor(value = "group-data-grid-styling.xml")
public class GroupDataGridStylingSample extends StandardView {

    @ViewComponent
    private GroupDataGrid<Customer> customersGroupDataGrid;

    @Subscribe
    private void onInit(InitEvent event) {
        DataGridColumn<Customer> group = customersGroupDataGrid.getColumnByKey("group");
        if (group != null) {
            group.setPartNameGenerator(customer ->
                    customer.getGrade() == null ? "" : "group-column-cell " + customer.getGrade().toString().toLowerCase());
        }
    }

    @Install(to = "customersGroupDataGrid", subject = "groupPartNameGenerator")
    private String onGroupPartNameGenerator(GroupInfo groupInfo) {
        GroupProperty property = groupInfo.getProperty();
        if (property.is("grade")) {
            return "group-grade" + " " + groupInfo.getValue().toString().toLowerCase();
        }
        return "";
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




group-data-grid-styling.css


vaadin-grid::part(group-grade premium),
vaadin-grid::part(group-column-cell premium) {
    background-color: #f3cff3;
}

vaadin-grid::part(group-grade high),
vaadin-grid::part(group-column-cell high) {
    background-color: #caccff;
}

vaadin-grid::part(group-grade standard),
vaadin-grid::part(group-column-cell standard) {
    background-color: #f0f0f0;
}


