<Path>Cookbook > Data in UI > Copying entities</Path>

This example demonstrates possible approaches to copying entities in list views. The view contains two actions: copy and copyAndEdit. The copy action creates a new instance and immediately saves it to the database. The copyAndEdit action creates a new instance and opens the entity detail, which saves the new instance only when the user clicks OK. Both actions use MetadataTools.copy() method to create a shallow copy of the selected entity instance.

copy-action.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_base">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e order by e.name]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox id="buttonsPanel" width="100%" wrap="true">
            <button id="customersDataGridCopyBtn" action="customersDataGrid.copy"/>
            <button id="customersDataGridCopyAndEditBtn" action="customersDataGrid.copyAndEdit"/>
            <button id="customersDataGridRefreshBtn" action="customersDataGrid.refresh"/>
        </hbox>
        <dataGrid id="customersDataGrid"
                  dataContainer="customersDc"
                  width="100%"
                  minHeight="20em">
            <actions>
                <action id="copy" text="Copy" icon="COPY" type="list_itemTracking"/>
                <action id="copyAndEdit" text="Copy and edit" icon="EDIT" type="list_itemTracking"/>
                <action id="refresh" type="list_refresh"/>
            </actions>
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




CopyActionSample.java

package io.jmix.uisamples.view.flowui.cookbook.copyaction;

import io.jmix.core.DataManager;
import io.jmix.core.MetadataTools;
import io.jmix.core.UuidProvider;
import io.jmix.flowui.DialogWindows;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.view.entity.customer.CustomerDetailView;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("copy-action")
@ViewDescriptor("copy-action.xml")
public class CopyActionSample extends StandardView {

    @ViewComponent
    protected CollectionContainer<Customer> customersDc;
    @ViewComponent
    protected DataGrid<Customer> customersDataGrid;

    @Autowired
    protected MetadataTools metadataTools;
    @Autowired
    protected DataManager dataManager;
    @Autowired
    protected DialogWindows dialogWindows;

    @Subscribe("customersDataGrid.copy")
    protected void onCustomersDataGridCopy(ActionPerformedEvent event) {
        Customer customer = customersDataGrid.getSingleSelectedItem();

        Customer customerCopy = createCopy(customer);

        Customer savedCopy = dataManager.save(customerCopy);
        customersDc.getMutableItems().add(0, savedCopy);
    }

    @Subscribe("customersDataGrid.copyAndEdit")
    protected void onCustomersTableCopyAndEdit(ActionPerformedEvent event) {
        Customer customer = customersDataGrid.getSingleSelectedItem();

        Customer customerCopy = createCopy(customer);

        dialogWindows.detail(customersDataGrid)
                .withViewClass(CustomerDetailView.class)
                .newEntity(customerCopy)
                .open();
    }

    protected Customer createCopy(Customer customer) {
        Customer customerCopy = metadataTools.copy(customer);
        customerCopy.setId(UuidProvider.createUuid());
        customerCopy.setName(StringUtils.abbreviate("Copy of " + customer.getName(), 50));
        return customerCopy;
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


