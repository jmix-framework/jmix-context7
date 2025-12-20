<Path>Components > DataGrid > DataGrid selection mode</Path>

selectionMode - sets the rows selection mode. There are four predefined selection modes: SINGLE - single record selection. MULTI - multiple selection using the embedded column with checkboxes. NONE - selection is disabled.

data-grid-selection-mode.xml

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
        <select id="selectionModeSelect" label="Selection mode"/>
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button id="greetAllBtn" action="customersDataGrid.greetAll"/>
            <button id="greetOneBtn" action="customersDataGrid.greetOne"/>
        </hbox>
        <dataGrid id="customersDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="customersDc">
            <actions>
                <action id="greetAll" type="list_itemTracking" icon="COMMENTS" text="Greet all"/>
                <action id="greetOne" type="list_itemTracking" icon="COMMENT" text="Greet single selected"/>
            </actions>
            <columns>
                <column property="name"/>
                <column property="lastName"/>
                <column property="email"/>
                <column property="age"/>
                <column property="active"/>
                <column property="grade"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridSelectionModeSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.selectionmode;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.grid.Grid;
import io.jmix.core.MetadataTools;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.component.select.JmixSelect;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Arrays;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;

@ViewController("data-grid-selection-mode")
@ViewDescriptor("data-grid-selection-mode.xml")
public class DataGridSelectionModeSample extends StandardView {

    @ViewComponent
    protected JmixSelect<Grid.SelectionMode> selectionModeSelect;
    @ViewComponent
    protected DataGrid<Customer> customersDataGrid;

    @Autowired
    protected Notifications notifications;
    @Autowired
    protected MetadataTools metadataTools;

    @Subscribe
    protected void onInit(InitEvent event) {
        ComponentUtils.setItemsMap(selectionModeSelect, getSelectionModeItemsMap());
        selectionModeSelect.setValue(Grid.SelectionMode.NONE);
    }

    @Subscribe("selectionModeSelect")
    protected void onSelectionModeValueChange(
            ComponentValueChangeEvent<JmixSelect<Grid.SelectionMode>, Grid.SelectionMode> event) {
        customersDataGrid.setSelectionMode(event.getValue());
    }

    @Subscribe("customersDataGrid.greetAll")
    protected void onCustomersDataGridGreetAllActionPerformed(ActionPerformedEvent event) {
        Set<Customer> customers = customersDataGrid.getSelectedItems();

        if (customers.isEmpty()) {
            notifications.show("No selection");
        } else {
            String greetString = customers.stream()
                    .map(metadataTools::getInstanceName)
                    .collect(Collectors.joining(", "));

            notifications.show("Hello, " + greetString);
        }
    }

    @Subscribe("customersDataGrid.greetOne")
    protected void onCustomersDataGridGreetOneActionPerformed(ActionPerformedEvent event) {
        Customer customer = customersDataGrid.getSingleSelectedItem();
        notifications.show(customer != null
                ? "Hello, " + metadataTools.getInstanceName(customer)
                : "No selection");
    }

    protected Map<Grid.SelectionMode, String> getSelectionModeItemsMap() {
        return Arrays.stream(Grid.SelectionMode.values())
                .collect(Collectors.toMap(Function.identity(), mode -> mode.name().replace('_', ' ')));
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


