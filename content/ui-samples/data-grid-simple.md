<Path>Components > DataGrid > Simple DataGrid</Path>

DataGrid is designed to display and sort tabular data, and provides means to manipulate rows. In this example, you can play with the following DataGrid settings: sortable - enables or disables the column sorting. The default value is true. When the sorting is enabled, the click on the column name will display the sorting icon to the right of the column header. Sorting of any specific column can be disabled by this column's sortable attribute. resizable - enables or disables the column resizing. The default value is false. columnReorderingAllowed - defines whether a user can change the columns order by dragging them with a mouse. The default value is false.

data-grid-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="ordersDc"
                    class="io.jmix.uisamples.entity.Order">
            <fetchPlan extends="_local">
                <property name="customer" fetchPlan="_local"/>
            </fetchPlan>
            <loader id="ordersLoader">
                <query>
                    <![CDATA[select e from uisamples_Order e order by e.date]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <checkboxGroup id="dataGridSettingsGroup" label="Settings"/>
        <dataGrid id="dataGrid" width="100%" minHeight="20em"
                  dataContainer="ordersDc">
            <columns>
                <column property="date"/>
                <column property="customer"/>
                <column property="amount"/>
                <column property="description"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridSimpleSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.simple;

import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Order;

import java.util.Collection;
import java.util.Collections;

@ViewController("data-grid-simple")
@ViewDescriptor("data-grid-simple.xml")
public class DataGridSimpleSample extends StandardView {

    @ViewComponent
    protected JmixCheckboxGroup<String> dataGridSettingsGroup;
    @ViewComponent
    protected DataGrid<Order> dataGrid;

    @Subscribe
    protected void onInit(InitEvent event) {
        initSettingsGroup();
    }

    protected void initSettingsGroup() {
        dataGridSettingsGroup.setItems("Sortable", "Resizable", "Column reordering allowed");
        dataGridSettingsGroup.setTypedValue(Collections.singletonList("Sortable"));
    }

    @Subscribe("dataGridSettingsGroup")
    protected void onDataGridSettingsGroupValueChange(
            TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        //clear
        dataGrid.getAllColumns().forEach(col -> {
            col.setSortable(false);
            col.setResizable(false);
        });
        dataGrid.setColumnReorderingAllowed(false);

        event.getValue()
                .forEach(this::applyGridSettings);
    }

    protected void applyGridSettings(String setting) {
        switch (setting) {
            case "Sortable" -> dataGrid.getAllColumns().forEach(col -> col.setSortable(true));
            case "Resizable" -> dataGrid.getAllColumns().forEach(col -> col.setResizable(true));
            case "Column reordering allowed" -> dataGrid.setColumnReorderingAllowed(true);
        }
    }
}




Order.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.UUID;

@Table(name = "ORDER")
@Entity(name = "uisamples_Order")
@JmixEntity
public class Order {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "CUSTOMER_ID")
    private Customer customer;

    @Temporal(TemporalType.DATE)
    @Column(name = "DATE_", nullable = false)
    @InstanceName
    private Date date;

    @Column(name = "AMOUNT")
    private BigDecimal amount;

    @Column(name = "DESCRIPTION")
    private String description;

    @OrderBy("rowNum")
    @Composition
    @OneToMany(mappedBy = "order")
    private List<OrderItem> items;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setItems(List<OrderItem> items) {
        this.items = items;
    }

    public List<OrderItem> getItems() {
        return items;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public Customer getCustomer() {
        return customer;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public Date getDate() {
        return date;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public BigDecimal getAmount() {
        return amount;
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


