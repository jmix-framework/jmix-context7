<Path>Components > DataGrid > DataGrid with context menu</Path>

The context menu in the DataGrid component is accessible by default by right-clicking. By default, the context menu duplicates actions associated with the component. To disable automatic generation of context menu elements, you can use the showInContextMenuEnabled attribute in the actions element. You can define your own context menu elements using the contextMenu element in the XML markup. To add an icon for a context menu element, you must use the icon attribute. To automatically assign icons of related actions to context menu elements, you can use the application property: jmix.ui.component.grid-context-menu-show-action-icons. It is also possible to customize the display of a context menu element using dynamicContentHandler.

data-grid-context-menu.xml

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
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button id="createBtn" action="customersDataGrid.create"/>
            <button id="editBtn" action="customersDataGrid.edit"/>
            <button id="removeBtn" action="customersDataGrid.remove"/>
            <button id="greetingBtn" action="customersDataGrid.greeting"/>
        </hbox>
        <dataGrid id="customersDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="customersDc">
            <contextMenu id="contextMenu">
                <item text="CRUD" icon="TABLE">
                    <item action="customersDataGrid.create" icon="PLUS"/>
                    <item action="customersDataGrid.edit" icon="PENCIL"/>
                    <item action="customersDataGrid.remove" icon="TRASH"/>
                </item>
                <item action="customersDataGrid.greeting" icon="COMMENT"/>
                <separator/>
                <item id="customerItem"/>
                <item action="customersDataGrid.getInfo" icon="INFO_CIRCLE_O"/>
            </contextMenu>
            <actions showInContextMenuEnabled="false">
                <action id="create" type="list_create">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                    </properties>
                </action>
                <action id="edit" type="list_edit">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                    </properties>
                </action>
                <action id="remove" type="list_remove"/>
                <action id="greeting" type="list_itemTracking" icon="COMMENT" text="Greeting"/>
                <action id="getInfo" type="list_itemTracking" icon="INFO_CIRCLE_O" text="Get info"/>
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




DataGridContextMenuSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.contextmenu;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.Html;
import com.vaadin.flow.component.grid.contextmenu.GridMenuItem;
import com.vaadin.flow.component.html.Span;
import io.jmix.core.MetadataTools;
import io.jmix.flowui.Dialogs;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("data-grid-context-menu")
@ViewDescriptor("data-grid-context-menu.xml")
public class DataGridContextMenuSample extends StandardView {

    @ViewComponent
    protected DataGrid<Customer> customersDataGrid;

    @Autowired
    protected Notifications notifications;
    @Autowired
    protected Dialogs dialogs;
    @Autowired
    protected MetadataTools metadataTools;

    @ViewComponent
    protected GridMenuItem<Customer> customerItem;

    @Install(to = "contextMenu", subject = "dynamicContentHandler")
    public boolean contextMenuDynamicContentHandler(Customer customer) {
        if (customer == null) {
            return false;
        }

        customerItem.setText(metadataTools.getInstanceName(customer));
        return true;
    }

    @Subscribe("customersDataGrid.greeting")
    public void onCustomersDataGridGreetingActionPerformed(ActionPerformedEvent event) {
        Customer customer = customersDataGrid.getSingleSelectedItem();

        notifications.show(customer != null
                ? "Hello, " + metadataTools.getInstanceName(customer)
                : "No selection");
    }

    @Subscribe("customersDataGrid.getInfo")
    public void onCustomersDataGridGetInfoActionPerformed(ActionPerformedEvent event) {
        Customer customer = customersDataGrid.getSingleSelectedItem();

        dialogs.createMessageDialog()
                .withContent(
                        customer != null
                                ? getMessageDialogContent(customer)
                                : new Span("No selection")
                )
                .open();
    }

    protected Component getMessageDialogContent(Customer customer) {
        return new Html("""
                <div>
                    <strong>Name:</strong> %s<br/>
                    <strong>Age:</strong> %s<br/>
                    <strong>Email:</strong> %s
                </div>
                """.formatted(metadataTools.getInstanceName(customer), customer.getAge(), customer.getEmail()));
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


