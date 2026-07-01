<Path>Components > DataGrid > DataGrid with ThemeVariant</Path>

The DataGrid component has several theme variants: column-borders no-border no-row-borders row-stripes wrap-cell-content You can set these styles to the DataGrid component using the themeNames attribute either in the XML descriptor or in the view controller using constants from GridVariant class.

data-grid-theme-variant.xml

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
        <hbox width="100%" wrap="true">
            <checkboxGroup id="gridSettingsCheckboxGroup" label="ThemeVariants" themeNames="horizontal"/>
        </hbox>
        <dataGrid id="ordersDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="ordersDc">
            <columns>
                <column property="customer"/>
                <column property="customer.grade"/>
                <column property="date"/>
                <column property="amount"/>
                <column property="description"/>
                <column property="items"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.themevariant;

import com.vaadin.flow.component.grid.GridVariant;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;

@ViewController("data-grid-theme-variant")
@ViewDescriptor("data-grid-theme-variant.xml")
public class DataGridThemeVariantSample extends StandardView {

    @ViewComponent
    private JmixCheckboxGroup<GridVariant> gridSettingsCheckboxGroup;
    @ViewComponent
    private DataGrid<Customer> ordersDataGrid;

    @Subscribe
    public void onInit(InitEvent event) {
        ComponentUtils.setItemsMap(gridSettingsCheckboxGroup, getGridThemeVariantItemsMap());
    }

    @Subscribe("gridSettingsCheckboxGroup")
    public void onGridSettingsCheckboxGroupValueChange(
            TypedValueChangeEvent<JmixCheckboxGroup<GridVariant>, Collection<GridVariant>> event) {
        if (event.getValue() == null) {
            return;
        }

        //clear
        ordersDataGrid.getElement().getThemeList().clear();

        event.getValue().forEach(ordersDataGrid::addThemeVariants);
    }

    private Map<GridVariant, String> getGridThemeVariantItemsMap() {
        LinkedHashMap<GridVariant, String> map = new LinkedHashMap<>();

        map.put(GridVariant.NO_BORDER, "No border");
        map.put(GridVariant.NO_ROW_BORDERS, "No row borders");
        map.put(GridVariant.COLUMN_BORDERS, "Column borders");
        map.put(GridVariant.ROW_STRIPES, "Row stripes");
        map.put(GridVariant.WRAP_CELL_CONTENT, "Wrap cell content");
        return map;
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


