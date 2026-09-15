<Path>Layouts > SidePanelLayout > SidePanelLayout as Master-detail</Path>

This example shows how to use `SidePanelLayout` as an entity editor.
    
A `CustomerMasterDetailFragment` is created dynamically and placed into the side panel for both
`CreateAction` and `EditAction` actions.
    
The fragment handles validation, save/cancel actions, and closes the panel after completion, while the host view
updates or reloads the `DataGrid`.


side-panel-layout-master-detail.xml

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
        <hbox>
            <button id="createButton" action="customersDataGrid.create"/>
            <button id="editButton" action="customersDataGrid.edit"/>
            <button id="removeButton" action="customersDataGrid.remove"/>
        </hbox>
        <sidePanelLayout id="sidePanelLayout" height="100%" width="100%"
                         sidePanelHorizontalSize="25em">
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
                    <column property="name"/>
                    <column property="lastName"/>
                    <column property="email"/>
                    <column property="age"/>
                    <column property="active"/>
                    <column property="grade"/>
                </columns>
            </dataGrid>
            <vbox id="sidePanelContent" height="100%" width="100%" padding="false"/>
        </sidePanelLayout>
    </layout>
</view>



SidePanelLayoutMasterDetailSample.java

package io.jmix.uisamples.view.flowui.containers.sidepanellayout.masterdetail;

import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.Fragments;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.component.sidepanellayout.SidePanelLayout;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.kit.component.sidepanellayout.SidePanelAfterOpenEvent;
import io.jmix.flowui.kit.component.sidepanellayout.SidePanelBeforeOpenEvent;
import io.jmix.flowui.kit.component.sidepanellayout.SidePanelCloseEvent;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("side-panel-layout-master-detail")
@ViewDescriptor("side-panel-layout-master-detail.xml")
public class SidePanelLayoutMasterDetailSample extends StandardView {

    @Autowired
    private Fragments fragments;

    @ViewComponent
    private VerticalLayout sidePanelContent;
    @ViewComponent
    private DataGrid<Customer> customersDataGrid;
    @ViewComponent
    private SidePanelLayout sidePanelLayout;

    @ViewComponent
    private CollectionContainer<Customer> customersDc;
    @ViewComponent
    private CollectionLoader<Customer> customersDl;

    @Subscribe("customersDataGrid.edit")
    public void onCustomersDataGridEdit(final ActionPerformedEvent event) {
        Customer item = customersDataGrid.getSingleSelectedItem();

        CustomerMasterDetailFragment editorFragment = createEditorFragment()
                .withEditedItem(item)
                .withSaveListener(saveEvent -> customersDc.replaceItem(saveEvent.getItem()));

        sidePanelContent.add(editorFragment);
        sidePanelLayout.openSidePanel();
    }

    @Subscribe("customersDataGrid.create")
    public void onCustomersDataGridCreate(final ActionPerformedEvent event) {
        CustomerMasterDetailFragment editorFragment = createEditorFragment()
                .withNewItem()
                .withSaveListener(saveEvent -> customersDl.load());

        sidePanelContent.add(editorFragment);
        sidePanelLayout.openSidePanel();
    }

    @Subscribe(id = "sidePanelLayout", subject = "addSidePanelBeforeOpenListener")
    public void onSidePanelLayoutBeforeOpen(SidePanelBeforeOpenEvent event) {
        setListActionsEnabled(false);
    }

    @Subscribe(id = "sidePanelLayout", subject = "addSidePanelAfterOpenListener")
    public void onSidePanelLayoutAfterOpened(SidePanelAfterOpenEvent event) {
        if (sidePanelContent.getComponentCount() == 0) {
            return;
        }

        CustomerMasterDetailFragment fragment = (CustomerMasterDetailFragment) sidePanelContent.getComponentAt(0);
        fragment.focusFirstField();
    }

    @Subscribe(id = "sidePanelLayout", subject = "addSidePanelCloseListener")
    public void onSidePanelLayoutClosed(SidePanelCloseEvent event) {
        sidePanelContent.removeAll();

        setListActionsEnabled(true);
    }

    private CustomerMasterDetailFragment createEditorFragment() {
        return fragments.create(this, CustomerMasterDetailFragment.class)
                .withSidePanelLayout(sidePanelLayout);
    }

    private void setListActionsEnabled(boolean enabled) {
        customersDataGrid.getActions().forEach(action -> action.setEnabled(enabled));
    }
}




customer-master-detail-fragment.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <data>
        <instance id="customerDc"
                    class="io.jmix.uisamples.entity.Customer"/>
    </data>
    <content>
        <vbox id="root" width="100%" height="100%">
            <hbox width="100%" justifyContent="BETWEEN" alignItems="CENTER">
                <h2 id="header" text="msg://header.text"/>
                <button id="closeButton" icon="lumo:cross" themeNames="tertiary icon contrast"/>
            </hbox>
            <scroller width="100%" height="100%" scrollBarsDirection="VERTICAL" classNames="p-s">
                <formLayout id="customerForm" dataContainer="customerDc"
                            autoResponsive="true" maxColumns="1"
                            expandColumns="true"
                            expandFields="true" width="100%">
                    <textField id="nameField" property="name"/>
                    <textField id="lastName" property="lastName"/>
                    <emailField id="emailField" property="email"/>
                    <textField id="ageField" property="age"/>
                    <checkbox id="activeField" property="active"/>
                    <select id="gradeField" property="grade"/>
                </formLayout>
            </scroller>
            <hbox>
                <button id="saveButton" text="msg:///actions.Save" themeNames="primary"/>
                <button id="cancelButton" text="msg:///actions.Cancel"/>
            </hbox>
        </vbox>
    </content>
</fragment>



CustomerMasterDetailFragment.java

package io.jmix.uisamples.view.flowui.containers.sidepanellayout.masterdetail;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.ComponentEvent;
import com.vaadin.flow.component.ComponentEventListener;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.TextField;
import io.jmix.core.DataManager;
import io.jmix.core.Id;
import io.jmix.flowui.component.UiComponentUtils;
import io.jmix.flowui.component.sidepanellayout.SidePanelLayout;
import io.jmix.flowui.component.validation.ValidationErrors;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.flowui.view.ViewValidation;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@FragmentDescriptor("customer-master-detail-fragment.xml")
public class CustomerMasterDetailFragment extends Fragment<VerticalLayout> {

    @Autowired
    private ViewValidation viewValidation;
    @Autowired
    private DataManager dataManager;

    @ViewComponent
    private InstanceContainer<Customer> customerDc;

    private SidePanelLayout sidePanelLayout;

    public CustomerMasterDetailFragment withSidePanelLayout(SidePanelLayout sidePanelLayout) {
        this.sidePanelLayout = sidePanelLayout;
        return this;
    }

    public CustomerMasterDetailFragment withNewItem() {
        customerDc.setItem(dataManager.create(Customer.class));
        return this;
    }

    public CustomerMasterDetailFragment withEditedItem(Customer customer) {
        customerDc.setItem(dataManager.load(Id.of(customer)).one());
        return this;
    }

    public CustomerMasterDetailFragment withSaveListener(ComponentEventListener<SaveEvent> listener) {
        addListener(SaveEvent.class, listener);
        return this;
    }

    public void focusFirstField() {
        UiComponentUtils.getComponents(getContent()).stream()
                .filter(c -> c instanceof TextField)
                .findFirst()
                .ifPresent(c -> ((TextField) c).focus());
    }

    public ValidationErrors validate() {
        return viewValidation.validateUiComponents(getContent());
    }

    @Subscribe(id = "saveButton", subject = "clickListener")
    public void onSaveButtonClick(final ClickEvent<JmixButton> event) {
        ValidationErrors errors = validate();
        if (errors.isEmpty()) {
            Customer saved = dataManager.save(customerDc.getItem());

            fireEvent(new SaveEvent(this, event.isFromClient(), saved));
            sidePanelLayout.closeSidePanel();
        } else {
            viewValidation.showValidationErrors(errors);
        }
    }

    @Subscribe(id = "cancelButton", subject = "clickListener")
    public void onCancelButtonClick(final ClickEvent<JmixButton> event) {
        sidePanelLayout.closeSidePanel();
    }

    @Subscribe(id = "closeButton", subject = "clickListener")
    public void onCloseButtonClick(final ClickEvent<JmixButton> event) {
        sidePanelLayout.closeSidePanel();
    }

    public static class SaveEvent extends ComponentEvent<CustomerMasterDetailFragment> {

        protected Customer item;

        public SaveEvent(CustomerMasterDetailFragment source,
                         boolean fromClient,
                         Customer item) {
            super(source, fromClient);

            this.item = item;
        }

        public Customer getItem() {
            return item;
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


