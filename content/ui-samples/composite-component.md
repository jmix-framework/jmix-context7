<Path>Custom components > Composite component</Path>

Composite components are created by combining existing components together. They encapsulate UI layout and behaviour and allow you to reuse identical parts of UI in different views. Composite components can contain data-aware components and load data themselves or rely on data containers provided by the host view. In this example, we demonstrate a composite component for editing addresses called AddressComponent. The component consists of several TypedTextField and EntityComboBox components representing the address parts. It works with the Address embeddable entity. The component's constructor accepts a few infrastructure beans and creates inner components and data containers. The initContent() method is invoked when the composite component is attached to the components tree. It adds its inner components to the parent component which is defined by the type parameter (Composite<FormLayout>). The composite component defines its own API method setDataContainer() which must be invoked after the component is created in a view. The method binds the inner components to the provided data container. After creating the composite component class, it can be used in views programmatically. See the initAddress() method of the AddressUsage class. To be able to use the new component in views XML declaratively, a few more steps are needed: Create an XSD for the component (see address-component.xsd). Implement the component loader (see AddressComponentLoader.java). Register the component and its loader in the application (see AddressComponentRegistration.java). Once these steps are completed, the composite component can be used in view XML descriptors. See the address-usage.xml file.

address-usage.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:address="http://io.jmix.uisamples/address-component.xsd">
    <data>
        <collection id="employeesDc"
                    class="io.jmix.uisamples.entity.Employee">
            <fetchPlan extends="_base">
                <property name="address" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="employeesLoader">
                <query>
                    <![CDATA[select e from Employee e order by e.firstName]]>
                </query>
            </loader>
        </collection>
        <instance id="employeeDc" class="io.jmix.uisamples.entity.Employee">
            <instance id="addressDc" property="address"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <select id="employeeSelect" label="Employee" itemsContainer="employeesDc"
                helperText="Select an employee whose address to display" minWidth="20em"/>
        <tabSheet id="tabSheet" width="100%">
            <tab id="declarative" label="msg://declarativeTab.label">
                <address:address id="addressComponent" dataContainer="addressDc"/>
            </tab>
        </tabSheet>
    </layout>
</view>



AddressUsage.java

package io.jmix.uisamples.view.flowui.customcomponents.composite;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.select.JmixSelect;
import io.jmix.flowui.component.tabsheet.JmixTabSheet;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.component.addresscomponent.AddressComponent;
import io.jmix.uisamples.entity.Address;
import io.jmix.uisamples.entity.Employee;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("composite-component")
@ViewDescriptor("address-usage.xml")
public class AddressUsage extends StandardView {

    @ViewComponent
    protected MessageBundle messageBundle;
    @ViewComponent
    protected InstanceContainer<Address> addressDc;
    @ViewComponent
    protected InstanceContainer<Employee> employeeDc;
    @ViewComponent
    protected JmixTabSheet tabSheet;

    @Autowired
    protected UiComponents uiComponents;

    @Subscribe
    protected void onInit(InitEvent event) {
        initAddress();
    }

    protected void initAddress() {
        AddressComponent addressComponent = uiComponents.create(AddressComponent.class);
        addressComponent.setDataContainer(addressDc);

        tabSheet.add(messageBundle.getMessage("programmaticTab.label"), addressComponent);
    }

    @Subscribe("employeeSelect")
    protected void onEmployeeSelectValueChange(ComponentValueChangeEvent<JmixSelect<Employee>, Employee> event) {
        employeeDc.setItem(event.getValue());
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

