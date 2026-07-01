<Path>Add-ons > GroupDataGrid > Group column attributes</Path>

groupIcon - specifies an icon to be displayed in the header of the group column. If you set the value to null, the default icon will be displayed. groupIconVisible - specifies whether to display the icon in the group column header. displayItemsCount - specifies whether to display the count of items in brackets for group rows. displayColumnsGrouperOnIconClick - specifies whether to display the Columns Grouper when the icon is clicked.

group-data-grid-column-attributes.xml

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
        <hbox padding="false" alignItems="CENTER">
            <comboBox id="groupIconsField" placeholder="msg://groupIconsField.placeholder" clearButtonVisible="true"/>
            <checkbox id="groupIconVisibleField" label="msg://groupIconVisibleField.label"/>
            <checkbox id="displayItemsCountField" label="msg://displayItemsCountField.label"/>
            <checkbox id="displayColumnsGrouperOnIconClickField" label="msg://displayColumnsGrouperOnIconClickField.label"/>
        </hbox>
        <groupg:groupDataGrid id="customersGroupDataGrid"
                              dataContainer="customersDc"
                              width="100%"
                              minHeight="20em">
            <groupg:groupBy>
                <groupg:columnRef key="grade"/>
            </groupg:groupBy>
            <groupg:columns>
                <groupg:groupColumn key="group" header="msg://customersGroupDataGrid.group.header" resizable="true"/>
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




GroupDataGridColumnAttributesSample.java

package io.jmix.uisamples.view.flowui.groupdatagrid.columnattributes;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.icon.VaadinIcon;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.view.*;
import io.jmix.groupgridflowui.component.GroupDataGrid;
import io.jmix.groupgridflowui.component.GroupDataGridColumn;
import io.jmix.uisamples.entity.Customer;

@ViewController("group-data-grid-column-attributes")
@ViewDescriptor(value = "group-data-grid-column-attributes.xml")
public class GroupDataGridColumnAttributesSample extends StandardView {

    @ViewComponent
    private JmixComboBox<VaadinIcon> groupIconsField;
    @ViewComponent
    private JmixCheckbox displayItemsCountField;
    @ViewComponent
    private JmixCheckbox displayColumnsGrouperOnIconClickField;
    @ViewComponent
    private JmixCheckbox groupIconVisibleField;

    @ViewComponent
    private GroupDataGrid<Customer> customersGroupDataGrid;

    private GroupDataGridColumn<Customer> groupColumn;

    @Subscribe
    public void onInit(InitEvent event) {
        groupColumn = (GroupDataGridColumn<Customer>) customersGroupDataGrid.getColumnByKey("group");

        groupIconsField.setItems(VaadinIcon.values());
        groupIconsField.setItemLabelGenerator(Enum::name);

        groupIconVisibleField.setValue(groupColumn.isGroupIconVisible());
        displayItemsCountField.setValue(groupColumn.isDisplayItemsCount());
        displayColumnsGrouperOnIconClickField.setValue(groupColumn.isDisplayColumnsGrouperOnIconClick());
    }

    @Subscribe("groupIconsField")
    public void onGroupIconsFieldValueChange(final ComponentValueChangeEvent<JmixComboBox<VaadinIcon>, VaadinIcon> event) {
        groupColumn.setGroupIcon(event.getValue() == null ? null : event.getValue().create());
    }

    @Subscribe("groupIconVisibleField")
    public void onGroupIconVisibleFieldValueChange(final ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        groupColumn.setGroupIconVisible(event.getValue());
    }

    @Subscribe("displayItemsCountField")
    public void onDisplayItemsCountFieldValueChange(final ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        groupColumn.setDisplayItemsCount(event.getValue());
        customersGroupDataGrid.getDataCommunicator().reset();
    }

    @Subscribe("displayColumnsGrouperOnIconClickField")
    public void onDisplayColumnsGrouperValueChange(final ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        groupColumn.setDisplayColumnsGrouperOnIconClick(event.getValue());
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




CustomerGrade.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.jspecify.annotations.Nullable;

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


