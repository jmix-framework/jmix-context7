<Path>Components > DataGrid > DataGrid with ItemDetails</Path>

The ItemDetails is a component that is using for showing the details for a specific row. You can set the details component for a DataGrid item using the setItemDetailsRenderer() method.

data-grid-item-details.xml

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
                  dataContainer="customersDc">
            <columns>
                <column property="name"/>
                <column property="lastName"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridItemDetailsSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.itemdetails;

import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.data.renderer.ComponentRenderer;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.bean.CustomerDetailsGenerator;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("data-grid-item-details")
@ViewDescriptor("data-grid-item-details.xml")
public class DataGridItemDetailsSample extends StandardView {

    @ViewComponent
    protected DataGrid<Customer> customersDataGrid;

    @Autowired
    protected CustomerDetailsGenerator detailsGenerator;

    @Subscribe
    protected void onInit(InitEvent event) {
        detailsGenerator.setReadOnlyMode(true);
        customersDataGrid.setItemDetailsRenderer(createCustomerDetailsRenderer());
    }

    protected ComponentRenderer<FormLayout, Customer> createCustomerDetailsRenderer() {
        return new ComponentRenderer<>(detailsGenerator::createCustomerDetailsRenderer, detailsGenerator::setCustomer);
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


