<Path>Components > DataGrid > DataGrid editor events</Path>

DataGrid has several events to listen for: EditorOpenEvent - fired when the DataGrid editor is opened. EditorCancelEvent - fired when editing is canceled. EditorCloseEvent - fired when the DataGrid editor is closed. EditorSaveEvent - fired when the DataGrid editor saves changes.

data-grid-editor-events.xml

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
        <dataGrid id="customersDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="customersDc"
                  editorBuffered="true">
            <columns>
                <column property="name" editable="true"/>
                <column property="lastName" editable="true"/>
                <column property="email"/>
                <column property="age"/>
                <column property="active"/>
                <column property="grade" editable="true"/>
                <editorActionsColumn key="bufferedEditorColumn">
                    <editButton icon="PENCIL" text="msg:///actions.Edit"/>
                    <saveButton icon="CHECK" themeNames="success"/>
                    <cancelButton icon="CLOSE" themeNames="error" text="msg:///actions.Cancel"/>
                </editorActionsColumn>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridEditorEventsSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.editorevents;

import com.vaadin.flow.component.grid.editor.EditorCancelEvent;
import com.vaadin.flow.component.grid.editor.EditorCloseEvent;
import com.vaadin.flow.component.grid.editor.EditorOpenEvent;
import com.vaadin.flow.component.grid.editor.EditorSaveEvent;
import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.Install;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("data-grid-editor-events")
@ViewDescriptor("data-grid-editor-events.xml")
public class DataGridEditorEventsSample extends StandardView {

    @Autowired
    protected Notifications notifications;

    @Install(to = "customersDataGrid.@editor", subject = "openListener")
    protected void onCustomersDataGridEditorOpened(EditorOpenEvent<Customer> event) {
        showNotification("Editor opened");
    }

    @Install(to = "customersDataGrid.@editor", subject = "cancelListener")
    protected void onCustomersDataGridEditorCanceled(EditorCancelEvent<Customer> event) {
        showNotification("Edit canceled");
    }

    @Install(to = "customersDataGrid.@editor", subject = "closeListener")
    protected void onCustomersDataGridEditorClosed(EditorCloseEvent<Customer> event) {
        showNotification("Editor closed");
    }

    @Install(to = "customersDataGrid.@editor", subject = "saveListener")
    protected void onCustomersDataGridEditorSaved(EditorSaveEvent<Customer> event) {
        showNotification("Changes saved");
    }

    protected void showNotification(String message) {
        notifications.create(message)
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


