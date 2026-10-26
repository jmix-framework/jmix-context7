<Path>Cookbook > Other recipes > Wizard</Path>

The sample shows a wizard, a dialog that guides the user through data entry step by step. The wizard creates an `Employee` entity (see `Employee.java`) and has three steps:

- basic information about the employee;
- address;
- confirmation of the entered data.

Each step is a `fragment`. The fragments declare the data containers of `WizardDialog` with `provided="true"` and bind their components to them in XML, so all steps work with the same `Employee` instance. The fields on the first two steps are validated before the wizard moves to the next step. The **Back** and **Next** buttons switch steps, and a click on a finished step returns to it.

The wizard is based on the `tabSheet` component, and each step is a tab. `WizardDialog` enables the tabs of the current and finished steps and disables the next ones. Based on this state, `wizard-dialog.css` turns the tabs into a step indicator: the selected tab is the current step, other enabled tabs are finished steps. The styles hide the tab background, connect the steps with lines, and highlight the finished and current steps with the accent color.

Useful links:

- [Composite Component]({contextPath}/sample/composite-component): the `AddressComponent` used on the second step;
- [Fragments]({contextPath}/sample/fragments): fragments that implement the steps.


wizard.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <button id="button" text="Open wizard" icon="MAGIC" themeNames="primary"/>
    </layout>
</view>




WizardSample.java

package io.jmix.uisamples.view.flowui.cookbook.wizard;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.DialogWindows;
import io.jmix.flowui.Fragments;
import io.jmix.flowui.icon.Icons;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.kit.icon.JmixFontIcon;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Employee;
import io.jmix.uisamples.view.flowui.cookbook.wizard.step.FirstStep;
import io.jmix.uisamples.view.flowui.cookbook.wizard.step.SecondStep;
import io.jmix.uisamples.view.flowui.cookbook.wizard.step.ThirdStep;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("wizard")
@ViewDescriptor("wizard.xml")
public class WizardSample extends StandardView {

    @Autowired
    private DialogWindows dialogWindows;
    @Autowired
    private Fragments fragments;
    @Autowired
    private Icons icons;

    @Subscribe(id = "button", subject = "clickListener")
    public void onButtonClick(final ClickEvent<JmixButton> event) {
        dialogWindows.detail(this, Employee.class)
                .newEntity()
                .withViewClass(WizardDialog.class)
                .withViewConfigurer(this::wizardConfigurer)
                .open();
    }

    private void wizardConfigurer(WizardDialog wizardDialog) {
        wizardDialog.addStep(
                        new WizardStep(icons.get(JmixFontIcon.USER_CARD), "Employee information",
                                fragments.create(wizardDialog, FirstStep.class))
                )
                .addStep(
                        new WizardStep(icons.get(JmixFontIcon.BUILDING), "Address",
                                fragments.create(wizardDialog, SecondStep.class))
                )
                .addStep(
                        new WizardStep(icons.get(JmixFontIcon.CHECK_CIRCLE), "Confirmation",
                                fragments.create(wizardDialog, ThirdStep.class))
                );
    }
}




WizardDialog.java

package io.jmix.uisamples.view.flowui.cookbook.wizard;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.tabs.Tab;
import io.jmix.flowui.component.tabsheet.JmixTabSheet;
import io.jmix.flowui.component.validation.ValidationErrors;
import io.jmix.flowui.icon.Icons;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.kit.icon.JmixFontIcon;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Employee;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("wizard-dialog")
@ViewDescriptor("wizard-dialog.xml")
@EditedEntityContainer("employeeDc")
@DialogMode(width = "50em")
public class WizardDialog extends StandardDetailView<Employee> {

    @ViewComponent
    private JmixTabSheet wizardContent;

    @ViewComponent
    private JmixButton backButton;
    @ViewComponent
    private JmixButton nextButton;

    @Autowired
    private ViewValidation viewValidation;
    @Autowired
    private Icons icons;

    @Subscribe
    public void onBeforeShow(final BeforeShowEvent event) {
        if (wizardContent.getTabCount() == 0) {
            throw new IllegalStateException("No steps added");
        }

        wizardContent.setSelectedIndex(0);

        updateStepsState();
        updateControlsState();
    }

    public WizardDialog addStep(WizardStep step) {
        wizardContent.add(createTab(step), step.content());

        updateStepsState();
        updateControlsState();
        return this;
    }

    @Subscribe("wizardContent")
    public void onWizardContentSelectedChange(final JmixTabSheet.SelectedChangeEvent event) {
        updateStepsState();
        updateControlsState();
    }

    @Subscribe(id = "backButton", subject = "clickListener")
    public void onBackButtonClick(final ClickEvent<JmixButton> event) {
        wizardContent.setSelectedIndex(wizardContent.getSelectedIndex() - 1);
    }

    @Subscribe(id = "nextButton", subject = "clickListener")
    public void onNextButtonClick(final ClickEvent<JmixButton> event) {
        if (isLastTabSelected()) {
            closeWithSave();
            return;
        }

        ValidationErrors validationErrors = validateCurrentStep();

        if (validationErrors.isEmpty()) {
            int nextIndex = wizardContent.getSelectedIndex() + 1;
            wizardContent.getTabAt(nextIndex).setEnabled(true);
            wizardContent.setSelectedIndex(nextIndex);
        } else {
            viewValidation.focusProblemComponent(validationErrors);
            viewValidation.showValidationErrors(validationErrors);
        }
    }

    private void updateStepsState() {
        int selectedIndex = wizardContent.getSelectedIndex();
        for (int i = 0; i < wizardContent.getTabCount(); i++) {
            wizardContent.getTabAt(i).setEnabled(i <= selectedIndex);
        }
    }

    private void updateControlsState() {
        backButton.setVisible(wizardContent.getSelectedIndex() != 0);

        if (isLastTabSelected()) {
            nextButton.setText("Complete");
            nextButton.setIcon(icons.get(JmixFontIcon.CHECK));
            nextButton.addThemeVariants(ButtonVariant.PRIMARY);
        } else {
            nextButton.setText("Next");
            nextButton.setIcon(icons.get(JmixFontIcon.ARROW_CIRCLE_RIGHT));
            nextButton.removeThemeVariants(ButtonVariant.PRIMARY);
        }
    }

    private boolean isLastTabSelected() {
        return wizardContent.getSelectedIndex() == wizardContent.getTabCount() - 1;
    }

    private ValidationErrors validateCurrentStep() {
        return viewValidation.validateUiComponents(wizardContent.getContentByTab(wizardContent.getSelectedTab()));
    }

    private Tab createTab(WizardStep step) {
        Div stepContent = new Div(step.icon(), new Span(step.text()));
        stepContent.addClassName("wizard-step");
        return new Tab(stepContent);
    }
}




wizard-dialog.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://wizardDialog.title">
    <data>
        <instance id="employeeDc" class="io.jmix.uisamples.entity.Employee">
            <fetchPlan extends="_base">
                <property name="address" fetchPlan="_base"/>
            </fetchPlan>
            <instance id="addressDc" property="address"/>
        </instance>
    </data>
    <layout classNames="wizard-dialog">
        <tabSheet id="wizardContent" themeNames="minimal" width="100%" height="100%"/>
        <hbox width="100%" justifyContent="END">
            <button id="backButton" text="Back" icon="ARROW_CIRCLE_LEFT"/>
            <button id="nextButton" text="Next" icon="ARROW_CIRCLE_RIGHT" iconAfterText="true"/>
        </hbox>
    </layout>
</view>




WizardStep.java

package io.jmix.uisamples.view.flowui.cookbook.wizard;

import com.vaadin.flow.component.Component;
import io.jmix.flowui.fragment.Fragment;

public record WizardStep(Component icon, String text, Fragment<?> content) {
}




wizard-dialog.css


.wizard-dialog vaadin-tabs {
    --vaadin-tabs-background: transparent;
}

.wizard-dialog vaadin-tab {
    --vaadin-tab-background: transparent;
    flex: 1 1 0;
    opacity: 1;
    cursor: default;
}

.wizard-dialog vaadin-tab[selected] {
    border-color: transparent;
    box-shadow: none;
}

.wizard-dialog vaadin-tab:not([disabled], [selected]) {
    cursor: var(--vaadin-clickable-cursor);
}

.wizard-dialog vaadin-tab:last-of-type {
    flex: none;
}

.wizard-dialog .wizard-step {
    display: flex;
    flex: 1;
    align-items: center;
    gap: var(--vaadin-gap-s);
    color: var(--vaadin-text-color-secondary);
}

.wizard-dialog .wizard-step::after {
    content: "";
    flex: 1;
    height: 1px;
    background-color: var(--vaadin-border-color);
}

.wizard-dialog vaadin-tab:last-of-type .wizard-step::after {
    display: none;
}

.wizard-dialog vaadin-tab:not([disabled]) .wizard-step {
    color: var(--vaadin-text-color);
}

.wizard-dialog vaadin-tab:not([disabled]) vaadin-icon {
    color: var(--aura-accent-color);
}

.wizard-dialog vaadin-tab:not([disabled], [selected]) .wizard-step::after {
    background-color: var(--aura-accent-color);
}

.wizard-dialog vaadin-tab:not([disabled], [selected]):hover .wizard-step {
    color: var(--aura-accent-text-color);
}




FirstStep.java

package io.jmix.uisamples.view.flowui.cookbook.wizard.step;

import io.jmix.flowui.component.formlayout.JmixFormLayout;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;

@FragmentDescriptor("first-step.xml")
public class FirstStep extends Fragment<JmixFormLayout> {
}




first-step.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <data>
        <instance id="employeeDc" class="io.jmix.uisamples.entity.Employee" provided="true"/>
    </data>
    <content>
        <formLayout dataContainer="employeeDc">
            <textField id="firstNameField" property="firstName"/>
            <textField id="lastNameField" property="lastName"/>
            <emailField id="emailField" property="email"/>
            <textField id="departmentField" property="department"/>
        </formLayout>
    </content>
</fragment>




SecondStep.java

package io.jmix.uisamples.view.flowui.cookbook.wizard.step;

import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;
import io.jmix.uisamples.component.addresscomponent.AddressComponent;

@FragmentDescriptor("second-step.xml")
public class SecondStep extends Fragment<AddressComponent> {
}




second-step.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment"
          xmlns:address="http://io.jmix.uisamples/address-component.xsd">
    <data>
        <instance id="addressDc" class="io.jmix.uisamples.entity.Address" provided="true"/>
    </data>
    <content>
        <address:address id="addressComponent" dataContainer="addressDc"/>
    </content>
</fragment>




AddressComponent.java

package io.jmix.uisamples.component.addresscomponent;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.Composite;
import io.jmix.core.DataManager;
import io.jmix.core.Sort;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.ComponentContainer;
import io.jmix.flowui.component.combobox.EntityComboBox;
import io.jmix.flowui.component.formlayout.JmixFormLayout;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.data.value.ContainerValueSource;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.model.DataComponents;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.uisamples.entity.Address;
import io.jmix.uisamples.entity.City;
import io.jmix.uisamples.entity.Country;

import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import static io.jmix.flowui.component.UiComponentUtils.sameId;

public class AddressComponent extends Composite<JmixFormLayout> implements ComponentContainer {

    protected final DataManager dataManager;
    private final CollectionContainer<Country> countriesContainer;
    private final CollectionContainer<City> citiesContainer;

    private final TypedTextField<String> zipField;
    private final EntityComboBox<Country> countryEntityComboBox;
    private final EntityComboBox<City> cityEntityComboBox;
    private final TypedTextField<String> addressLine;

    @SuppressWarnings({"unchecked"})
    public AddressComponent(UiComponents uiComponents, DataComponents dataComponents, DataManager dataManager) {
        this.dataManager = dataManager;

        zipField = uiComponents.create(TypedTextField.class);
        zipField.setMaxLength(32);
        zipField.setLabel("Zip");

        countryEntityComboBox = uiComponents.create(EntityComboBox.class);
        countryEntityComboBox.setLabel("Country");

        cityEntityComboBox = uiComponents.create(EntityComboBox.class);
        cityEntityComboBox.setLabel("City");

        addressLine = uiComponents.create(TypedTextField.class);
        addressLine.setLabel("Address Line");

        countriesContainer = dataComponents.createCollectionContainer(Country.class);
        countriesContainer.addItemChangeListener(countryItemChangeEvent -> loadCities());
        countryEntityComboBox.setItems(countriesContainer);

        citiesContainer = dataComponents.createCollectionContainer(City.class);
        cityEntityComboBox.setItems(citiesContainer);
    }

    private void loadCountries() {
        List<Country> countries = dataManager.load(Country.class).all().sort(Sort.by("name")).list();
        countriesContainer.setItems(countries);
    }

    private void loadCities() {
        List<City> cities = dataManager.load(City.class)
                .query("e.country = ?1", countriesContainer.getItemOrNull())
                .list();
        citiesContainer.setItems(cities);
    }

    @Override
    protected JmixFormLayout initContent() {
        JmixFormLayout content = super.initContent();
        content.add(zipField, countryEntityComboBox, cityEntityComboBox, addressLine);
        return content;
    }

    public void setDataContainer(InstanceContainer<Address> instanceContainer) {
        zipField.setValueSource(new ContainerValueSource<>(instanceContainer, "zip"));
        addressLine.setValueSource(new ContainerValueSource<>(instanceContainer, "addressLine"));
        countryEntityComboBox.setValueSource(new ContainerValueSource<>(instanceContainer, "country"));
        cityEntityComboBox.setValueSource(new ContainerValueSource<>(instanceContainer, "city"));

        loadCountries();
        loadCities();
    }

    @Override
    public Optional<Component> findOwnComponent(String id) {
        return getChildren()
                .filter(component -> sameId(component, id))
                .findFirst();
    }

    @Override
    public Collection<Component> getOwnComponents() {
        return getChildren().sequential().collect(Collectors.toList());
    }
}




address-component.xsd

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xs:schema xmlns="http://io.jmix.uisamples/address-component.xsd"
           elementFormDefault="qualified"
           targetNamespace="http://io.jmix.uisamples/address-component.xsd"
           xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:layout="http://jmix.io/schema/flowui/layout">

    <xs:element name="address">
        <xs:complexType>
            <xs:complexContent>
                <xs:extension base="layout:baseComponent">
                    <xs:attribute name="dataContainer" type="xs:string"/>
                </xs:extension>
            </xs:complexContent>
        </xs:complexType>
    </xs:element>
</xs:schema>



AddressComponentLoader.java

package io.jmix.uisamples.component.addresscomponent;

import io.jmix.flowui.exception.GuiDevelopmentException;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.xml.layout.loader.AbstractComponentLoader;
import io.jmix.uisamples.entity.Address;
import org.dom4j.Element;

public class AddressComponentLoader extends AbstractComponentLoader<AddressComponent> {

    @Override
    protected AddressComponent createComponent() {
        return factory.create(AddressComponent.class);
    }

    @Override
    public void loadComponent() {
        loadDataContainer(resultComponent, element);
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    protected void loadDataContainer(AddressComponent resultComponent, Element element) {
        String dataContainerIsNullErrorMessage = String.format(
                "%s doesn't have data binding. Set dataContainer attribute.",
                resultComponent.getClass().getSimpleName()
        );
        String containerId = loadString(element, "dataContainer")
                .orElseThrow(() -> new GuiDevelopmentException(dataContainerIsNullErrorMessage, context));

        InstanceContainer container = getContext().getDataHolder().getContainer(containerId);
        if (!Address.class.isAssignableFrom(container.getEntityMetaClass().getJavaClass())) {
            String improperDataBindingMessage = String.format(
                    "%s have improper data binding. The value for the " +
                            "dataContainer attribute should be associated with the Address embeddable entity.",
                    resultComponent.getClass().getSimpleName());
            throw new GuiDevelopmentException(improperDataBindingMessage, context);
        }

        resultComponent.setDataContainer(container);
    }
}




AddressComponentRegistration.java

package io.jmix.uisamples.view.flowui.customcomponents.composite;

import io.jmix.flowui.sys.registration.ComponentRegistration;
import io.jmix.flowui.sys.registration.ComponentRegistrationBuilder;
import io.jmix.uisamples.component.addresscomponent.AddressComponent;
import io.jmix.uisamples.component.addresscomponent.AddressComponentLoader;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AddressComponentRegistration {

    @Bean
    public ComponentRegistration address() {
        return ComponentRegistrationBuilder.create(AddressComponent.class)
                .withComponentLoader("address", AddressComponentLoader.class)
                .build();
    }
}




ThirdStep.java

package io.jmix.uisamples.view.flowui.cookbook.wizard.step;

import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;

@FragmentDescriptor("third-step.xml")
public class ThirdStep extends Fragment<VerticalLayout> {
}




third-step.css


.third-step .reminder {
    color: var(--vaadin-text-color-secondary);
}

.third-step .grid-container {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    grid-template-rows: repeat(2, minmax(0, 1fr));
    column-gap: var(--vaadin-gap-s);
}

.third-step .bold {
    font-weight: 700;
}




third-step.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <data>
        <instance id="employeeDc" class="io.jmix.uisamples.entity.Employee" provided="true"/>
        <instance id="addressDc" class="io.jmix.uisamples.entity.Address" provided="true"/>
    </data>
    <content>
        <vbox padding="false" spacing="false" classNames="third-step">
            <h4 text="Employee information confirmation"/>
            <span text="Please check the information before saving" classNames="reminder"/>
            <hr width="100%"/>
            <div classNames="grid-container">
                <span text="First name:" classNames="bold"/>
                <span dataContainer="employeeDc" property="firstName"/>
                <span text="Last name:" classNames="bold"/>
                <span dataContainer="employeeDc" property="lastName"/>
                <span text="Email:" classNames="bold"/>
                <span dataContainer="employeeDc" property="email"/>
                <span text="Department:" classNames="bold"/>
                <span dataContainer="employeeDc" property="department"/>
            </div>
            <hr width="100%"/>
            <div classNames="grid-container">
                <span text="Zip:" classNames="bold"/>
                <span dataContainer="addressDc" property="zip"/>
                <span text="Country:" classNames="bold"/>
                <span dataContainer="addressDc" property="country"/>
                <span text="City:" classNames="bold"/>
                <span dataContainer="addressDc" property="city"/>
                <span text="Address Line:" classNames="bold"/>
                <span dataContainer="addressDc" property="addressLine"/>
            </div>
        </vbox>
    </content>
</fragment>




Employee.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.EmbeddedParameters;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@JmixEntity
@Table(name = "EMPLOYEE")
@Entity
public class Employee {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "DEPARTMENT")
    private String department;

    @Column(name = "FIRST_NAME", nullable = false)
    @NotNull
    private String firstName;

    @Column(name = "LAST_NAME", nullable = false)
    @NotNull
    private String lastName;

    @Email
    @Column(name = "EMAIL")
    protected String email;

    @EmbeddedParameters(nullAllowed = false)
    @Embedded
    @AssociationOverrides({
            @AssociationOverride(name = "country", joinColumns = @JoinColumn(name = "ADDRESS_COUNTRY_ID")),
            @AssociationOverride(name = "city", joinColumns = @JoinColumn(name = "ADDRESS_CITY_ID"))
    })
    @AttributeOverrides({
            @AttributeOverride(name = "zip", column = @Column(name = "ADDRESS_ZIP")),
            @AttributeOverride(name = "addressLine", column = @Column(name = "ADDRESS_ADDRESS_LINE"))
    })
    private Address address;

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(final String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(final String email) {
        this.email = email;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    @InstanceName
    @DependsOnProperties({"firstName", "lastName"})
    public String getDisplayName() {
        return String.format("%s %s", (firstName != null ? firstName : ""),
                (lastName != null ? lastName : ""));
    }
}



Address.java

package io.jmix.uisamples.entity;

import io.jmix.core.MetadataTools;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

@JmixEntity
@Embeddable
public class Address {

    @Column(name = "ZIP")
    private String zip;

    @JoinColumn(name = "COUNTRY_ID", nullable = false)
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Country country;

    @JoinColumn(name = "CITY_ID", nullable = false)
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private City city;

    @Column(name = "ADDRESS_LINE")
    private String addressLine;

    public String getAddressLine() {
        return addressLine;
    }

    public void setAddressLine(String addressLine) {
        this.addressLine = addressLine;
    }

    public City getCity() {
        return city;
    }

    public void setCity(City city) {
        this.city = city;
    }

    public Country getCountry() {
        return country;
    }

    public void setCountry(Country country) {
        this.country = country;
    }

    public String getZip() {
        return zip;
    }

    public void setZip(String zip) {
        this.zip = zip;
    }

    @InstanceName
    @DependsOnProperties({"zip", "country", "city", "addressLine"})
    public String getInstanceName(MetadataTools metadataTools) {
        return String.format("%s %s %s %s",
                metadataTools.format(zip),
                metadataTools.format(country),
                metadataTools.format(city),
                metadataTools.format(addressLine));
    }
}



Country.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@JmixEntity
@Table(name = "COUNTRY")
@Entity
public class Country {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private Integer id;

    @InstanceName
    @Column(name = "NAME")
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}



City.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

@JmixEntity
@Table(name = "CITY", indexes = {
        @Index(name = "IDX_CITY_COUNTRY", columnList = "COUNTRY_ID")
})
@Entity
public class City {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private Integer id;

    @JoinColumn(name = "COUNTRY_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private Country country;

    @InstanceName
    @Column(name = "NAME")
    private String name;

    public Country getCountry() {
        return country;
    }

    public void setCountry(Country country) {
        this.country = country;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}

