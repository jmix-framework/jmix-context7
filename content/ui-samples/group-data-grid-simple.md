<Path>Add-ons > GroupDataGrid > Simple GroupDataGrid</Path>

GroupDataGrid is a Grid component that supports grouping data items by specific entity properties. The component includes GroupDataGridColumn, which displays the grouping and provides a toggler for each group. By default, the column header shows a group icon that manages the grouping column when clicked. To perform grouping declaratively, use the groupBy element, which columns will be grouped.

group-data-grid-simple.xml

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
                <groupg:groupColumn header="msg://customersGroupDataGrid.group.header" resizable="true"/>
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




GroupDataGridSimpleSample.java

package io.jmix.uisamples.view.flowui.groupdatagrid.simple;

import io.jmix.flowui.view.*;

@ViewController("group-data-grid-simple")
@ViewDescriptor(value = "group-data-grid-simple.xml")
public class GroupDataGridSimpleSample extends StandardView {
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


