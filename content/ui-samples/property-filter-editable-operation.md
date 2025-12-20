<Path>Components > PropertyFilter > PropertyFilter with editable operation</Path>

operationEditable attribute sets whether an operation selector is visible. If the value is true component enables the selection of the condition in run-time. The list of available operators depends on the attribute type. PropertyFilter provides the ability to subscribe to OperationChangeEvent. It is thrown when the operation is changed.

property-filter-editable-operation.xml

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
        <propertyFilter id="propertyFilter"
                        property="name"
                        operation="CONTAINS"
                        operationEditable="true"
                        dataLoader="customersDl"/>
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




PropertyFilterEditableOperationSample.java

package io.jmix.uisamples.view.flowui.components.propertyfilter.editableoperation;

import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.propertyfilter.PropertyFilter;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("property-filter-editable-operation")
@ViewDescriptor("property-filter-editable-operation.xml")
public class PropertyFilterEditableOperationSample extends StandardView {

    @Autowired
    protected Notifications notifications;

    @Subscribe("propertyFilter")
    protected void onPropertyFilterOperationChange(PropertyFilter.OperationChangeEvent<Customer> event) {
        notifications.create("Prev: " + event.getPreviousOperation().name() + ", New: " + event.getNewOperation().name())
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
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


