<Path>Components > DataGrid > DataGrid frozen column</Path>

A column can be frozen using the frozen attribute. frozen - column is frozen in-place, freeze columns from left to right for a consistent outcome. frozenToEnd - column is frozen in-place, freeze columns from right to left for a consistent outcome.

data-grid-frozen-column.xml

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
        <span text="Change the size of the columns to see the frozen column."/>
        <hbox classNames="buttons-panel items-center">
            <select id="columnSelect" placeholder="Column to freeze"/>
            <hbox id="checkboxPlaceholder" padding="false"/>
        </hbox>
        <dataGrid id="customersDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="customersDc">
            <columns>
                <column property="name" width="13em" resizable="true"/>
                <column property="lastName" width="13em" resizable="true"/>
                <column property="email" width="13em" resizable="true"/>
                <column property="age" width="13em" resizable="true"/>
                <column property="active" width="13em" resizable="true"/>
                <column property="grade" width="13em" resizable="true"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridFrozenColumnSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.frozencolumn;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.component.select.JmixSelect;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@ViewController("data-grid-frozen-column")
@ViewDescriptor("data-grid-frozen-column.xml")
public class DataGridFrozenColumnSample extends StandardView {

    @ViewComponent
    protected HorizontalLayout checkboxPlaceholder;
    @ViewComponent
    protected JmixSelect<Grid.Column<Customer>> columnSelect;
    @ViewComponent
    protected DataGrid<Customer> customersDataGrid;

    @Autowired
    protected UiComponents uiComponents;

    @Subscribe
    protected void onInit(InitEvent event) {
        ComponentUtils.setItemsMap(columnSelect, getColumnItemsMap());
    }

    @Subscribe("columnSelect")
    protected void onColumnSelectChange(
            ComponentValueChangeEvent<JmixSelect<Grid.Column<Customer>>, Grid.Column<Customer>> event) {
        checkboxPlaceholder.removeAll();

        Grid.Column<Customer> column = event.getValue();
        checkboxPlaceholder.add(createFrozenCheckbox(column), createFrozenToEndCheckbox(column));
    }

    protected Map<Grid.Column<Customer>, String> getColumnItemsMap() {
        return customersDataGrid.getAllColumns().stream()
                .collect(Collectors.toMap(Function.identity(),Grid.Column::getHeaderText));
    }

    protected JmixCheckbox createFrozenCheckbox(Grid.Column<Customer> column) {
        JmixCheckbox frozenCheckbox = uiComponents.create(JmixCheckbox.class);
        frozenCheckbox.setLabel("Frozen");
        frozenCheckbox.setValue(column.isFrozen());

        frozenCheckbox.addValueChangeListener(event -> column.setFrozen(event.getValue()));

        return frozenCheckbox;
    }

    protected JmixCheckbox createFrozenToEndCheckbox(Grid.Column<Customer> column) {
        JmixCheckbox frozenCheckbox = uiComponents.create(JmixCheckbox.class);
        frozenCheckbox.setLabel("Frozen To End");
        frozenCheckbox.setValue(column.isFrozenToEnd());

        frozenCheckbox.addValueChangeListener(event -> column.setFrozenToEnd(event.getValue()));

        return frozenCheckbox;
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


