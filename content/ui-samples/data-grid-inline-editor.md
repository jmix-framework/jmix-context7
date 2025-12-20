<Path>Components > DataGrid > DataGrid inline editor</Path>

This sample demonstrates how to provide inline editing in a `DataGrid` component.

To make a column editable, set its `editable` attribute to `true`. The `editorActionsColumn` element creates an additional column with buttons to control the inline editing.

This example illustrates two editing modes using two data grids on separate tabs:

- In _non-buffered_ mode (the default), inline edit fields directly update the entity attributes. The `editorActionsColumn` element should include a `closeButton`.

- In _buffered_ mode, users can confirm or discard changes in the edited row. The `editorActionsColumn` element should include the `saveButton` and `cancelButton`, which save or discard changes to the entity attributes. Buffered mode is enabled by setting the `editorBuffered` attribute of the `dataGrid` component to `true`.  

The example also demonstrates saving changes to the database. Depending on the state of the **Save immediately** checkbox, changes are saved right after closing the inline editor for each row or when the user clicks the **Save** button.

Changed entities are either saved immediately or queued for later processing using listeners on the `DataGridEditor` object. Listeners can be configured using `@Install` annotations or added programmatically via `dataGrid.getEditor().addSaveListener()` and similar methods. The simplest way is to use the **Handlers** tab of the Jmix Studio's **Component Inspector**, where editor event listeners are marked with `[Editor]` prefixes. 

data-grid-inline-editor.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_local">
            <loader id="customersDl" readOnly="true">
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
        <hbox alignItems="CENTER" width="100%" justifyContent="END">
            <checkbox id="immediateCheckbox" label="Save immediately" value="true"/>
            <button id="saveButton" text="Save" enabled="false"/>
        </hbox>
        <tabSheet width="100%" height="100%">
            <tab id="nonBufferedTab" label="Non-buffered editor">
                <dataGrid id="customersDataGridNonBuffered"
                          width="100%"
                          height="100%"
                          minHeight="20em"
                          dataContainer="customersDc">
                    <columns>
                        <column property="name" editable="true"/>
                        <column property="lastName" editable="true"/>
                        <column property="email"/>
                        <column property="age"/>
                        <column property="active"/>
                        <column property="grade" editable="true"/>
                        <editorActionsColumn key="nonBufferedEditorColumn">
                            <editButton icon="PENCIL" text="msg:///actions.Edit"/>
                            <closeButton icon="CHECK"/>
                        </editorActionsColumn>
                    </columns>
                </dataGrid>
            </tab>
            <tab id="bufferedTab" label="Buffered editor">
                <dataGrid id="customersDataGridBuffered"
                          width="100%"
                          height="100%"
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
            </tab>
        </tabSheet>
    </layout>
</view>




DataGridInlineEditorSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.inlineeditor;

import com.vaadin.flow.component.AbstractField;
import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.grid.editor.EditorCloseEvent;
import com.vaadin.flow.component.grid.editor.EditorSaveEvent;
import io.jmix.core.DataManager;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.HashSet;
import java.util.Set;

@ViewController("data-grid-inline-editor")
@ViewDescriptor("data-grid-inline-editor.xml")
public class DataGridInlineEditorSample extends StandardView {

    @Autowired
    private DataManager dataManager;
    @Autowired
    private Notifications notifications;

    @ViewComponent
    private CollectionContainer<Customer> customersDc;
    @ViewComponent
    private CollectionLoader<Customer> customersDl;
    @ViewComponent
    private JmixCheckbox immediateCheckbox;
    @ViewComponent
    private JmixButton saveButton;

    private final Set<Customer> changedCustomers = new HashSet<>();

    @Install(to = "customersDataGridBuffered.@editor", subject = "saveListener")
    private void customersDataGridBufferedEditorSaveListener(final EditorSaveEvent<Customer> event) {
        saveOrEnqueue(event.getItem());
    }

    @Install(to = "customersDataGridNonBuffered.@editor", subject = "closeListener")
    private void customersDataGridNonBufferedEditorCloseListener(final EditorCloseEvent<Customer> event) {
        saveOrEnqueue(event.getItem());
    }

    @Subscribe("immediateCheckbox")
    public void onImmediateCheckboxComponentValueChange(final AbstractField.ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        saveButton.setEnabled(!event.getValue());
    }

    @Subscribe(id = "saveButton", subject = "clickListener")
    public void onSaveButtonClick(final ClickEvent<JmixButton> event) {
        saveEnqueuedChanges();
    }

    private void saveOrEnqueue(Customer customer) {

        if (immediateCheckbox.getValue()) {
            saveChanges(customer);
        } else {
            changedCustomers.add(customer);
        }
    }

    private void saveChanges(Customer customer) {
        // Save changed entity
        Customer savedCustomer = dataManager.save(customer);
        // Replace the original entity in the data container with the saved one
        customersDc.replaceItem(savedCustomer);
        // Note that if the original entity is merged into DataContext (this is the
        // case when <loader readOnly="false">), the saved instance should be merged too
        notifications.show("Changes saved to the database");
    }

    private void saveEnqueuedChanges() {
        if (!changedCustomers.isEmpty()) {
            // Save enqueued changes. The returned value is ignored because all data will be reloaded.
            dataManager.saveAll(changedCustomers);
            changedCustomers.clear();
            notifications.show("Changes saved to the database");
            customersDl.load();
        }
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


