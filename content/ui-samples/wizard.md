<Path>Cookbook > Other recipes > Wizard</Path>

Wizard is a component for step-by-step data filling. This example demonstrates the wizard for creating the Employee entity (see Employee.java). The wizard opens in the dialog by clicking the button and consists of three steps: Filling in basic information about the employee Filling in the address Checking the entered information Each step is associated with data, information about which is stored in the main view WizardDialog. The first two steps have fields that will be validated when moving to the next step. The user can switch between steps at any time (if the data at the current step is correct) using the corresponding buttons, which change their behavior and state depending on the current step. The wizard is based on the tabSheet component. The steps are implemented as separate tabs. The content of each tab is implemented as a fragment. Useful links: Composite Component – implementation of the AddressComponent component, which is used in the second step Fragments – a composite component, which is used to create steps

wizard.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <button id="button" text="Open wizard" icon="MAGIC" themeNames="primary"/>
    </layout>
</view>




WizardSample.java

package io.jmix.uisamples.view.flowui.cookbook.wizard;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.icon.VaadinIcon;
import io.jmix.flowui.DialogWindows;
import io.jmix.flowui.Fragments;
import io.jmix.flowui.kit.component.button.JmixButton;
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
                        new WizardStep<>(VaadinIcon.USER_CARD.create(), "Employee information",
                                fragments.create(wizardDialog, FirstStep.class))
                )
                .addStep(
                        new WizardStep<>(VaadinIcon.BUILDING.create(), "Address",
                                fragments.create(wizardDialog, SecondStep.class))
                )
                .addStep(
                        new WizardStep<>(VaadinIcon.CHECK_CIRCLE_O.create(), "Confirmation",
                                fragments.create(wizardDialog, ThirdStep.class))
                );
    }
}




WizardDialog.java

package io.jmix.uisamples.view.flowui.cookbook.wizard;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.ThemableLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.tabs.Tab;
import io.jmix.flowui.component.tabsheet.JmixTabSheet;
import io.jmix.flowui.component.validation.ValidationErrors;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Employee;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.function.Supplier;

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

    private int tabsCount;

    @Subscribe
    public void onBeforeShow(final BeforeShowEvent event) {
        if (tabsCount == 0) {
            throw new IllegalStateException("No steps added");
        }

        wizardContent.getTabAt(0).setEnabled(true);
        wizardContent.setSelectedIndex(0);

        updateControlsState();
    }

    public WizardDialog addStep(WizardStep<?> step) {
        Tab tab = createTab(step, ++tabsCount);
        tab.setEnabled(false);
        step.content().setupData(getViewData());
        wizardContent.add(tab, step.content());
        return this;
    }

    @Subscribe("wizardContent")
    public void onWizardContentSelectedChange(final JmixTabSheet.SelectedChangeEvent event) {
        updateControlsState();
    }

    @Subscribe(id = "backButton", subject = "clickListener")
    public void onBackButtonClick(final ClickEvent<JmixButton> event) {
        wizardContent.getSelectedTab().setEnabled(false);
        int selectedIndex = wizardContent.getSelectedIndex();
        wizardContent.getTabAt(--selectedIndex).setEnabled(true);
        wizardContent.setSelectedIndex(selectedIndex);
    }

    @Subscribe(id = "nextButton", subject = "clickListener")
    public void onNextButtonClick(final ClickEvent<JmixButton> event) {
        if (isLastTabSelected()) {
            closeWithSave();
            return;
        }

        ValidationErrors validationErrors = validateCurrentStep();

        if (validationErrors.isEmpty()) {
            wizardContent.getSelectedTab().setEnabled(false);
            int selectedIndex = wizardContent.getSelectedIndex();
            wizardContent.getTabAt(++selectedIndex).setEnabled(true);
            wizardContent.setSelectedIndex(selectedIndex);
        } else {
            viewValidation.focusProblemComponent(validationErrors);
            viewValidation.showValidationErrors(validationErrors);
        }
    }

    private void updateControlsState() {
        backButton.setVisible(wizardContent.getSelectedIndex() != 0);

        if (isLastTabSelected()) {
            nextButton.setText("Complete");
            nextButton.setIcon(VaadinIcon.CHECK.create());
            nextButton.addThemeVariants(ButtonVariant.PRIMARY);
        } else {
            nextButton.setText("Next");
            nextButton.setIcon(VaadinIcon.ARROW_CIRCLE_RIGHT_O.create());
            nextButton.removeThemeVariants(ButtonVariant.PRIMARY);
        }
    }

    private boolean isLastTabSelected() {
        return wizardContent.getSelectedIndex() == tabsCount - 1;
    }

    private ValidationErrors validateCurrentStep() {
        return viewValidation.validateUiComponents(wizardContent.getContentByTab(wizardContent.getSelectedTab()));
    }

    private Tab createTab(WizardStep<?> step, int index) {
        VerticalLayout layout = createLayout(VerticalLayout::new);
        layout.setAlignItems(FlexComponent.Alignment.CENTER);
        layout.addClassName("tab-container");

        HorizontalLayout horizontalLayout = createLayout(HorizontalLayout::new);
        horizontalLayout.addClassName("label-container");

        Span label = new Span("Step #" + index);
        label.addClassName("label");
        horizontalLayout.add(step.icon(), label);

        Span text = new Span(step.text());
        text.addClassNames("sublabel");

        layout.add(horizontalLayout, text);

        return new Tab(layout);
    }

    private <T extends ThemableLayout & FlexComponent> T createLayout(Supplier<T> factory) {
        T layout = factory.get();
        layout.setPadding(false);
        layout.setSpacing(false);
        return layout;
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
        <tabSheet id="wizardContent" themeNames="equal-width-tabs"
                  width="100%" height="100%"/>
        <hbox width="100%" justifyContent="END">
            <button id="backButton" text="Back" icon="ARROW_CIRCLE_LEFT_O"/>
            <button id="nextButton" text="Next" icon="ARROW_CIRCLE_RIGHT_O" iconAfterText="true"/>
        </hbox>
    </layout>
</view>




WizardStep.java

package io.jmix.uisamples.view.flowui.cookbook.wizard;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.icon.Icon;

public record WizardStep<T extends Component & WizardStepFragment>(Icon icon, String text, T content) {
}




wizard-dialog.css


.wizard-dialog .tab-container {
    line-height: var(--aura-line-height-m);
}

.wizard-dialog .label-container {
    gap: var(--vaadin-gap-xs);
}

.wizard-dialog .label {
    font-size: var(--aura-font-size-s);
}

.wizard-dialog .sublabel {
    font-size: var(--aura-font-size-s);
    color: var(--vaadin-text-color-secondary);
}




WizardStepFragment.java

package io.jmix.uisamples.view.flowui.cookbook.wizard;

import io.jmix.flowui.model.ViewData;

public interface WizardStepFragment {

    void setupData(ViewData viewData);
}




FirstStep.java

package io.jmix.uisamples.view.flowui.cookbook.wizard.step;

import com.vaadin.flow.component.Component;
import io.jmix.flowui.component.ComponentContainer;
import io.jmix.flowui.component.formlayout.JmixFormLayout;
import io.jmix.flowui.data.SupportsValueSource;
import io.jmix.flowui.data.value.ContainerValueSource;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;
import io.jmix.flowui.fragment.FragmentUtils;
import io.jmix.flowui.model.ViewData;
import io.jmix.uisamples.view.flowui.cookbook.wizard.WizardStepFragment;

import java.util.Collection;
import java.util.Optional;

@FragmentDescriptor("first-step.xml")
public class FirstStep extends Fragment<JmixFormLayout>
        implements WizardStepFragment, ComponentContainer {

    public void setupData(ViewData viewData) {
        getOwnComponents().forEach(component -> {
            if (component instanceof SupportsValueSource<?> valueSourceComponent) {
                valueSourceComponent.setValueSource(
                        new ContainerValueSource<>(viewData.getContainer("employeeDc"),
                                FragmentUtils.getComponentId(component).orElseThrow())
                );
            }
        });
    }

    @Override
    public Optional<Component> findOwnComponent(String id) {
        return getContent().findOwnComponent(id);
    }

    @Override
    public Collection<Component> getOwnComponents() {
        return getContent().getOwnComponents();
    }
}




first-step.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <content>
        <formLayout>
            <textField id="firstName" label="First name"/>
            <textField id="lastName" label="Last name"/>
            <emailField id="email" label="Email"/>
            <textField id="department" label="Department"/>
        </formLayout>
    </content>
</fragment>




SecondStep.java

package io.jmix.uisamples.view.flowui.cookbook.wizard.step;

import com.vaadin.flow.component.Component;
import io.jmix.flowui.component.ComponentContainer;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.model.ViewData;
import io.jmix.uisamples.component.addresscomponent.AddressComponent;
import io.jmix.uisamples.view.flowui.cookbook.wizard.WizardStepFragment;

import java.util.Collection;
import java.util.Optional;

public class SecondStep extends Fragment<AddressComponent>
        implements WizardStepFragment, ComponentContainer {

    @Override
    public void setupData(ViewData viewData) {
        getContent().setDataContainer(viewData.getContainer("addressDc"));
    }

    @Override
    public Optional<Component> findOwnComponent(String id) {
        return getContent().getContent().findOwnComponent(id);
    }

    @Override
    public Collection<Component> getOwnComponents() {
        return getContent().getContent().getOwnComponents();
    }
}




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




ThirdStep.java

package io.jmix.uisamples.view.flowui.cookbook.wizard.step;

import com.vaadin.flow.component.HtmlContainer;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.data.binding.HtmlContainerReadonlyDataBinding;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;
import io.jmix.flowui.fragment.FragmentUtils;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.model.ViewData;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.uisamples.entity.Employee;
import io.jmix.uisamples.view.flowui.cookbook.wizard.WizardStepFragment;
import org.springframework.beans.factory.annotation.Autowired;

@FragmentDescriptor("third-step.xml")
public class ThirdStep extends Fragment<VerticalLayout> implements WizardStepFragment {

    @Autowired
    private HtmlContainerReadonlyDataBinding htmlDataBinding;

    @ViewComponent
    private Div employeeData;
    @ViewComponent
    private Div addressData;

    @Override
    public void setupData(ViewData viewData) {
        InstanceContainer<Employee> employeeDc = viewData.getContainer("employeeDc");
        InstanceContainer<Employee> addressDc = viewData.getContainer("addressDc");

        bindChildData(employeeData, employeeDc);
        bindChildData(addressData, addressDc);
    }

    private void bindChildData(Div div, InstanceContainer<?> dataContainer) {
        div.getChildren().forEach(component -> {
            if (component instanceof HtmlContainer htmlContainer) {
                FragmentUtils.getComponentId(htmlContainer)
                        .ifPresent(id -> bindHtmlContainer(htmlContainer, id, dataContainer));
            }
        });
    }

    private void bindHtmlContainer(HtmlContainer htmlContainer, String id, InstanceContainer<?> dataContainer) {
        htmlDataBinding.bind(htmlContainer, dataContainer, id);
    }
}




third-step.css


.third-step .reminded {
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
    <content>
        <vbox padding="false" spacing="false" classNames="third-step">
            <h4 text="Employee information confirmation"/>
            <span text="Please check the information before saving" classNames="reminder"/>
            <hr width="100%"/>
            <div id="employeeData" classNames="grid-container">
                <span text="First name:" classNames="bold"/>
                <span id="firstName"/>
                <span text="Last name" classNames="bold"/>
                <span id="lastName"/>
                <span text="Email:" classNames="bold"/>
                <span id="email"/>
                <span text="Department:" classNames="bold"/>
                <span id="department"/>
            </div>
            <hr width="100%"/>
            <div id="addressData" classNames="grid-container">
                <span text="Zip:" classNames="bold"/>
                <span id="zip"/>
                <span text="Country:" classNames="bold"/>
                <span id="country"/>
                <span text="City:" classNames="bold"/>
                <span id="city"/>
                <span text="Address Line:" classNames="bold"/>
                <span id="addressLine"/>
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

