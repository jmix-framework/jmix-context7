<Path>Components > GenericFilter > GenericFilter with multiple conditions</Path>

The GenericFilter component enables quick data filtering by arbitrary conditions, as well as creating configurations for repeated use. Configuration can be created in design-time (DesignTimeConfiguration) or in run-time (RunTimeConfiguration). Design-time configurations cannot be changed, but can be copied in run-time using the Copy action from the drop-down menu of filter settings. In this example, the configuration was created in design-time in XML, made default using default XML attribute. So it appears right after opening the screen. You can add conditions to this configuration by copying it, or reset it by selecting Reset filter in the drop-down menu next to the Refresh button and create a new configuration. New conditions can be saved for future use by clicking Save, Save with values or Save as in the settings drop-down menu.

generic-filter-multiple-conditions.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_local">
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
        <genericFilter id="genericFilter" dataLoader="customersDl">
            <properties include=".*"/>
            <configurations>
                <configuration id="defaultConfiguration" name="Configuration with multiple conditions"
                               default="true">
                    <propertyFilter property="age" operation="GREATER_OR_EQUAL"
                                    operationEditable="true" defaultValue="30"/>
                    <propertyFilter property="grade" operation="EQUAL"
                                    operationEditable="true" defaultValue="20"/>
                    <propertyFilter property="active" operation="EQUAL"
                                    operationEditable="true" defaultValue="true"/>
                </configuration>
            </configurations>
        </genericFilter>
        <dataGrid id="customersDataGrid"
                  dataContainer="customersDc"
                  width="100%"
                  minHeight="20em">
            <columns>
                <column property="name"/>
                <column property="lastName"/>
                <column property="age"/>
                <column property="active"/>
                <column property="grade"/>
            </columns>
        </dataGrid>
    </layout>
</view>




GenericFilterMultipleConditionsSample.java

package io.jmix.uisamples.view.flowui.components.genericfilter.multiple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("generic-filter-multiple-conditions")
@ViewDescriptor("generic-filter-multiple-conditions.xml")
public class GenericFilterMultipleConditionsSample extends StandardView {
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


