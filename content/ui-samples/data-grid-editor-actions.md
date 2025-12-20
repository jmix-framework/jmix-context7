<Path>Components > DataGrid > DataGrid with overridden actions</Path>

This example demonstrates the override of standard Create and Edit actions so that instead of opening the edit screen, the DataGrid inline editor is used

data-grid-editor-actions.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
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
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button id="createBtn" action="customersDataGrid.create"/>
            <button id="editBtn" action="customersDataGrid.edit"/>
            <button id="removeBtn" action="customersDataGrid.remove"/>
        </hbox>
        <dataGrid id="customersDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="customersDc">
            <actions>
                <action id="create" type="list_create"/>
                <action id="edit" type="list_edit"/>
                <action id="remove" type="list_remove"/>
            </actions>
            <columns>
                <column property="name" editable="true"/>
                <column property="lastName" editable="true"/>
                <column property="email" editable="true"/>
                <column property="age" editable="true"/>
                <column property="active" editable="true"/>
                <column property="grade" editable="true"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridEditorActionsSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.editoractions;

import io.jmix.core.Metadata;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("data-grid-editor-actions")
@ViewDescriptor("data-grid-editor-actions.xml")
public class DataGridEditorActionsSample extends StandardView {

    @ViewComponent
    protected DataGrid<Customer> customersDataGrid;
    @ViewComponent
    protected CollectionContainer<Customer> customersDc;

    @Autowired
    protected Notifications notifications;
    @Autowired
    protected Metadata metadata;

    @Subscribe("customersDataGrid.create")
    protected void onCustomersDataGridCreate(ActionPerformedEvent event) {
        if (customersDataGrid.getEditor().isOpen()) {
            showNotification("Close the editor before creating a new entity");
        } else {
            Customer newCustomer = metadata.create(Customer.class);
            customersDc.getMutableItems().add(newCustomer);
            customersDataGrid.select(newCustomer);
            customersDataGrid.getEditor().editItem(newCustomer);
        }
    }

    @Subscribe("customersDataGrid.edit")
    protected void onCustomersDataGridEdit(ActionPerformedEvent event) {
        Customer selectedCustomer = customersDataGrid.getSingleSelectedItem();

        if (selectedCustomer != null && !customersDataGrid.getEditor().isOpen()) {
            customersDataGrid.getEditor().editItem(selectedCustomer);
        } else {
            showNotification("The editor is already open");
        }
    }

    protected void showNotification(String message) {
        notifications.create(message)
                .withType(Notifications.Type.WARNING)
                .withCloseable(false)
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


