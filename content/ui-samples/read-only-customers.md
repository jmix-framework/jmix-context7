<Path>Cookbook > Data in UI > Using database view</Path>

This example demonstrates usage of a database view in the list view. The Customer entity is mapped to the CUSTOMER table which stores information about customers. The ReadOnlyCustomer entity is mapped to the CUSTOMER_VIEW database view defined as follows: create view CUSTOMER_VIEW as select ID, NAME || ' ' || LAST_NAME as FULL_NAME, AGE from CUSTOMER The read-only-customers.xml view defines data components and table to load and display data from the database view using the ReadOnlyCustomer entity. Obviously, this entity cannot be used to edit data. So the table actions have custom handlers in the ReadOnlyCustomersSample controller to edit data using the Customer entity. The action handlers use the DialogWindows bean to open the Customer edit screen and reload data in the table after successful commit.

read-only-customers.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="readOnlyCustomersDc"
                    class="io.jmix.uisamples.entity.ReadOnlyCustomer">
            <fetchPlan extends="_base"/>
            <loader id="readOnlyCustomersDl">
                <query>
                    <![CDATA[select e from ReadOnlyCustomer e order by e.fullName]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox id="buttonsPanel" width="100%" wrap="true">
            <button id="createBtn" action="readOnlyCustomersDataGrid.create"/>
            <button id="editBtn" action="readOnlyCustomersDataGrid.edit"/>
            <button id="removeBtn" action="readOnlyCustomersDataGrid.remove"/>
        </hbox>
        <dataGrid id="readOnlyCustomersDataGrid"
                  dataContainer="readOnlyCustomersDc"
                  width="100%"
                  minHeight="20em">
            <actions>
                <action id="create" type="list_create"/>
                <action id="edit" type="list_edit"/>
                <action id="remove" type="list_remove"/>
            </actions>
            <columns>
                <column property="fullName"/>
                <column property="age"/>
            </columns>
        </dataGrid>
    </layout>
</view>





ReadOnlyCustomersSample.java

package io.jmix.uisamples.view.flowui.cookbook.readonlycustomers;

import io.jmix.core.DataManager;
import io.jmix.core.Id;
import io.jmix.flowui.DialogWindows;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.ReadOnlyCustomer;
import io.jmix.uisamples.view.entity.customer.CustomerDetailView;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("read-only-customers")
@ViewDescriptor("read-only-customers.xml")
public class ReadOnlyCustomersSample extends StandardView {

    @ViewComponent
    protected CollectionLoader<ReadOnlyCustomer> readOnlyCustomersDl;
    @ViewComponent
    protected DataGrid<ReadOnlyCustomer> readOnlyCustomersDataGrid;

    @Autowired
    protected DialogWindows screenBuilders;
    @Autowired
    protected DataManager dataManager;

    @Subscribe("readOnlyCustomersDataGrid.create")
    protected void onReadOnlyCustomersDataGridCreate(ActionPerformedEvent event) {
        screenBuilders.detail(this, Customer.class)
                .newEntity()
                .withViewClass(CustomerDetailView.class)
                .withAfterCloseListener(afterCloseEvent -> {
                    if (afterCloseEvent.closedWith(StandardOutcome.SAVE)) {
                        readOnlyCustomersDl.load();
                    }
                })
                .open();
    }

    @Subscribe("readOnlyCustomersDataGrid.edit")
    protected void onReadOnlyCustomersDataGridEdit(ActionPerformedEvent event) {
        ReadOnlyCustomer readOnlyCustomer = readOnlyCustomersDataGrid.getSingleSelectedItem();
        if (readOnlyCustomer == null) {
            return;
        }

        Customer customer = dataManager.load(Customer.class).id(readOnlyCustomer.getId()).one();

        screenBuilders.detail(this, Customer.class)
                .editEntity(customer)
                .withViewClass(CustomerDetailView.class)
                .withAfterCloseListener(afterCloseEvent -> {
                    if (afterCloseEvent.closedWith(StandardOutcome.SAVE)) {
                        readOnlyCustomersDl.load();
                    }
                })
                .open();
    }

    @Subscribe("readOnlyCustomersDataGrid.remove")
    protected void onReadOnlyCustomersDataGridRemove(ActionPerformedEvent event) {
        ReadOnlyCustomer readOnlyCustomer = readOnlyCustomersDataGrid.getSingleSelectedItem();
        if (readOnlyCustomer == null) {
            return;
        }

        dataManager.remove(Id.of(readOnlyCustomer.getId(), Customer.class));
        readOnlyCustomersDl.load();
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




ReadOnlyCustomer.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import io.jmix.data.DbView;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.UUID;

@Table(name = "CUSTOMER_VIEW")
@Entity
@JmixEntity
@DbView
public class ReadOnlyCustomer {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @InstanceName
    @Column(name = "FULL_NAME")
    protected String fullName;

    @Column(name = "AGE")
    protected Integer age;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}


