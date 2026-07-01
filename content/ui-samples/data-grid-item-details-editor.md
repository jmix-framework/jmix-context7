<Path>Components > DataGrid > DataGrid with ItemDetails editor</Path>

The ItemDetails can be used to edit an item in DataGrid. This sample shows one way to implement this feature.

data-grid-item-details-editor.xml

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
        <hbox id="buttonsPanel" width="100%" wrap="true">
            <button id="createBtn" action="customersDataGrid.create"/>
            <button id="editBtn" action="customersDataGrid.edit"/>
            <button id="removeBtn" action="customersDataGrid.remove"/>
        </hbox>
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
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridItemDetailsEditorSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.itemdetailseditor;

import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.data.renderer.ComponentRenderer;
import io.jmix.core.Metadata;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.bean.CustomerDetailsEditorGenerator;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("data-grid-item-details-editor")
@ViewDescriptor("data-grid-item-details-editor.xml")
public class DataGridItemDetailsEditorSample extends StandardView {

    @ViewComponent
    protected DataGrid<Customer> customersDataGrid;
    @ViewComponent
    protected CollectionContainer<Customer> customersDc;

    @Autowired
    protected CustomerDetailsEditorGenerator detailsEditorGenerator;
    @Autowired
    protected Metadata metadata;
    @Autowired
    protected Notifications notifications;

    @Subscribe
    protected void onInit(InitEvent event) {
        detailsEditorGenerator.setCustomersDataGrid(customersDataGrid);
        customersDataGrid.setItemDetailsRenderer(createCustomerDetailsRenderer());
        customersDataGrid.setDetailsVisibleOnClick(false);
    }

    protected ComponentRenderer<VerticalLayout, Customer> createCustomerDetailsRenderer() {
        return new ComponentRenderer<>(
                detailsEditorGenerator::createDetailsEditorComponent,
                detailsEditorGenerator::setEditedEntity
        );
    }

    @Subscribe("customersDataGrid.create")
    protected void onCustomersDataGridCreate(ActionPerformedEvent event) {
        if (customersDataGrid.isDetailsVisible(customersDataGrid.getSingleSelectedItem())) {
            showNotification("Close the editor before creating a new entity");
        } else {
            Customer newCustomer = metadata.create(Customer.class);
            customersDc.getMutableItems().add(newCustomer);
            customersDataGrid.select(newCustomer);
            customersDataGrid.setDetailsVisible(newCustomer, true);
        }
    }

    @Subscribe("customersDataGrid.edit")
    protected void onCustomersDataGridEdit(ActionPerformedEvent event) {
        Customer selectedCustomer = customersDataGrid.getSingleSelectedItem();

        if (selectedCustomer != null && !customersDataGrid.isDetailsVisible(selectedCustomer)) {
            customersDataGrid.setDetailsVisible(selectedCustomer, true);
        } else {
            showNotification("The editor is already open");
        }
    }

    protected void showNotification(String message) {
        notifications.create(message)
                .withType(Notifications.Type.WARNING)
                .withCloseable(false)
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




CustomerDetailsGenerator.java

package io.jmix.uisamples.bean;

import com.vaadin.flow.component.HasLabel;
import com.vaadin.flow.component.HasValue;
import com.vaadin.flow.component.formlayout.FormLayout;
import io.jmix.core.MessageTools;
import io.jmix.core.Metadata;
import io.jmix.core.metamodel.model.MetaClass;
import io.jmix.core.metamodel.model.MetaProperty;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.ComponentGenerationContext;
import io.jmix.flowui.component.UiComponentsGenerator;
import io.jmix.flowui.data.SupportsValueSource;
import io.jmix.flowui.data.value.ContainerValueSource;
import io.jmix.flowui.model.DataComponents;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Scope(BeanDefinition.SCOPE_PROTOTYPE)
@Component("uisamples_CustomerDetailsGenerator")
public class CustomerDetailsGenerator {

    protected UiComponents uiComponents;
    protected UiComponentsGenerator componentsGenerator;
    protected DataComponents dataComponents;
    protected MessageTools messageTools;

    protected MetaClass metaClass;

    protected boolean readOnlyMode;

    public CustomerDetailsGenerator(UiComponents uiComponents,
                                    Metadata metadata,
                                    UiComponentsGenerator componentsGenerator,
                                    DataComponents dataComponents,
                                    MessageTools messageTools) {
        this.uiComponents = uiComponents;
        this.componentsGenerator = componentsGenerator;
        this.dataComponents = dataComponents;
        this.messageTools = messageTools;

        this.metaClass = metadata.getClass(Customer.class);
    }

    public FormLayout createCustomerDetailsRenderer() {
        FormLayout formLayout = uiComponents.create(FormLayout.class);
        formLayout.setResponsiveSteps(new FormLayout.ResponsiveStep("0", 2));

        generateComponent(formLayout, metaClass.getProperty("name"));
        generateComponent(formLayout, metaClass.getProperty("lastName"));
        generateComponent(formLayout, metaClass.getProperty("grade"));
        generateComponent(formLayout, metaClass.getProperty("active"));
        generateComponent(formLayout, metaClass.getProperty("email"));
        generateComponent(formLayout, metaClass.getProperty("age"));

        return formLayout;
    }

    protected void generateComponent(FormLayout formLayout, MetaProperty metaProperty) {
        ComponentGenerationContext componentGenerationContext =
                new ComponentGenerationContext(metaClass, metaProperty.getName());

        com.vaadin.flow.component.Component generatedComponent =
                componentsGenerator.generate(componentGenerationContext);
        generatedComponent.setId(metaProperty.getName() + "Field");

        formLayout.add(generatedComponent);
    }

    public void setCustomer(FormLayout formLayout, Customer customer) {
        InstanceContainer<Customer> instanceContainer = dataComponents.createInstanceContainer(Customer.class);
        instanceContainer.setItem(customer);

        formLayout.getChildren()
                .forEach(component -> setValueToComponent(component, instanceContainer));
    }

    protected void setValueToComponent(com.vaadin.flow.component.Component component,
                                       InstanceContainer<Customer> instanceContainer) {
        if (component.getId().isEmpty()) {
            return;
        }

        String id = component.getId().get();
        String propertyName = id.replace("Field", "");

        if (component instanceof SupportsValueSource<?> valueSourceComponent) {
            valueSourceComponent.setValueSource(new ContainerValueSource<>(instanceContainer, propertyName));
        }

        if (component instanceof HasLabel hasLabelComponent) {
            MetaClass metaClass = instanceContainer.getEntityMetaClass();
            hasLabelComponent.setLabel(messageTools.getPropertyCaption(metaClass, propertyName));
        }

        if (component instanceof HasValue<?, ?> hasValueComponent) {
            hasValueComponent.setReadOnly(readOnlyMode);
        }
    }

    public void setReadOnlyMode(boolean readOnlyMode) {
        this.readOnlyMode = readOnlyMode;
    }
}




CustomerDetailsEditorGenerator.java

package io.jmix.uisamples.bean;

import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.core.DataManager;
import io.jmix.core.EntityStates;
import io.jmix.core.Metadata;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.component.validation.ValidationErrors;
import io.jmix.flowui.data.grid.ContainerDataGridItems;
import io.jmix.flowui.icon.Icons;
import io.jmix.flowui.kit.action.Action;
import io.jmix.flowui.kit.action.ActionVariant;
import io.jmix.flowui.kit.action.BaseAction;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.kit.icon.JmixFontIcon;
import io.jmix.flowui.view.ViewValidation;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Scope(BeanDefinition.SCOPE_PROTOTYPE)
@Component("uisamples_CustomerDetailsEditorGenerator")
public class CustomerDetailsEditorGenerator {

    protected UiComponents uiComponents;
    protected CustomerDetailsGenerator detailsGenerator;
    protected DataManager dataManager;
    protected Metadata metadata;
    protected ViewValidation viewValidation;
    protected EntityStates entityStates;
    protected Icons icons;

    protected DataGrid<Customer> customersDataGrid;

    public CustomerDetailsEditorGenerator(UiComponents uiComponents,
                                          CustomerDetailsGenerator detailsGenerator,
                                          DataManager dataManager,
                                          Metadata metadata,
                                          ViewValidation viewValidation,
                                          EntityStates entityStates,
                                          Icons icons) {
        this.uiComponents = uiComponents;
        this.detailsGenerator = detailsGenerator;
        this.dataManager = dataManager;
        this.metadata = metadata;
        this.viewValidation = viewValidation;
        this.entityStates = entityStates;
        this.icons = icons;
    }

    public VerticalLayout createDetailsEditorComponent() {
        VerticalLayout verticalLayout = uiComponents.create(VerticalLayout.class);
        verticalLayout.setPadding(false);
        verticalLayout.addComponentAsFirst(detailsGenerator.createCustomerDetailsRenderer());
        return verticalLayout;
    }

    public void setEditedEntity(VerticalLayout verticalLayout, Customer customer) {
        Customer bufferCustomer = metadata.create(Customer.class);
        copy(customer, bufferCustomer);
        detailsGenerator.setCustomer((FormLayout) verticalLayout.getComponentAt(0), bufferCustomer);

        GenerationContext generationContext = new GenerationContext(customer, bufferCustomer, verticalLayout);
        verticalLayout.add(createDetailsButtonPanel(generationContext));
    }

    protected HorizontalLayout createDetailsButtonPanel(GenerationContext context) {
        HorizontalLayout layout = uiComponents.create(HorizontalLayout.class);
        layout.setPadding(false);

        layout.add(createSaveAndCloseButton(context), createCancelButton(context.initialCustomer()));
        return layout;
    }

    protected JmixButton createSaveAndCloseButton(GenerationContext context) {
        JmixButton button = uiComponents.create(JmixButton.class);
        button.setAction(createSaveAndCloseAction(context));

        return button;
    }

    protected JmixButton createCancelButton(Customer customer) {
        JmixButton button = uiComponents.create(JmixButton.class);
        button.setAction(createCancelAction(customer));

        return button;
    }

    protected Action createSaveAndCloseAction(GenerationContext context) {
        return new BaseAction("ok")
                .withText("OK")
                .withIcon(icons.get(JmixFontIcon.CHECK))
                .withVariant(ActionVariant.PRIMARY)
                .withHandler(e -> {
                    ValidationErrors validationErrors = validate(context.mainLayout());
                    if (validationErrors.isEmpty()) {
                        Customer customer = context.initialCustomer();
                        copy(context.bufferCustomer(), customer);

                        dataManager.save(customer);
                        customersDataGrid.setDetailsVisible(customer, false);
                    } else {
                        viewValidation.showValidationErrors(validationErrors);
                    }
                });
    }

    protected Action createCancelAction(Customer customer) {
        return new BaseAction("cancel")
                .withText("Cancel")
                .withIcon(icons.get(JmixFontIcon.BAN))
                .withHandler(e -> {
                    customersDataGrid.setDetailsVisible(customer, false);

                    if (entityStates.isNew(customer)
                            && customersDataGrid.getDataProvider() instanceof ContainerDataGridItems<?> items) {
                        items.getContainer().getMutableItems().remove(customer);
                    }
                });
    }

    protected void copy(Customer copyFrom, Customer copyTo) {
        copyTo.setName(copyFrom.getName());
        copyTo.setLastName(copyFrom.getLastName());
        copyTo.setGrade(copyFrom.getGrade());
        copyTo.setActive(copyFrom.isActive());
        copyTo.setEmail(copyFrom.getEmail());
        copyTo.setAge(copyFrom.getAge());
    }

    protected ValidationErrors validate(com.vaadin.flow.component.Component mainLayout) {
        return viewValidation.validateUiComponents(mainLayout);
    }

    protected record GenerationContext(Customer initialCustomer,
                                       Customer bufferCustomer,
                                       VerticalLayout mainLayout) {
    }

    public void setCustomersDataGrid(DataGrid<Customer> customersDataGrid) {
        this.customersDataGrid = customersDataGrid;
    }
}

