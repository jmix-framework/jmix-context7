<Path>Fragments > Fragment with data</Path>

Fragments, like views, can work with data. This is done using the <data/> tag in the fragment descriptor. A fragment can have its own data containers and loaders, defined in the <data/> XML element. At the same time, the framework creates a single instance of DataContext for the view and all its fragments. Therefore, all loaded entities are merged to the same context and their changes are saved when the host view is committed. Data components defined with provided="true" attribute which means that the container with the same id must exist in a host view or enclosing fragment, i.e. it must be provided from outside. In this sample, a InstanceContainer is defined in the host view. In the fragment, a InstanceContainer has been created with the same ID and provided="true" attribute. Thus, the host-view container will be used in the fragment.

fragment-data.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="employeesDc"
                    class="io.jmix.uisamples.entity.Employee">
            <fetchPlan extends="_base">
                <property name="address" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="employeesDl">
                <query>
                    <![CDATA[select e from Employee e order by e.firstName]]>
                </query>
            </loader>
        </collection>
        <instance id="addressDc" class="io.jmix.uisamples.entity.Address"/>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <select id="employeeSelect" label="Employee" itemsContainer="employeesDc"
                helperText="Select an employee whose address to display" minWidth="20em"/>
        <fragment class="io.jmix.uisamples.view.flowui.fragments.data.AddressFragment"/>
    </layout>
</view>




FragmentDataSample.java

package io.jmix.uisamples.view.flowui.fragments.data;

import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Address;
import io.jmix.uisamples.entity.Employee;

@ViewController("fragment-data")
@ViewDescriptor("fragment-data.xml")
public class FragmentDataSample extends StandardView {

    @ViewComponent
    protected InstanceContainer<Address> addressDc;

    @Subscribe(id = "employeesDc", target = Target.DATA_CONTAINER)
    public void onEmployeesDcItemChange(final InstanceContainer.ItemChangeEvent<Employee> event) {
        if (event.getItem() != null) {
            addressDc.setItem(event.getItem().getAddress());
        }
    }
}




address-fragment.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <data>
        <instance id="addressDc" class="io.jmix.uisamples.entity.Address"
                  fetchPlan="_base"
                  provided="true"/>
        <collection id="countryDc" class="io.jmix.uisamples.entity.Country"
                    fetchPlan="_base">
            <loader id="countryDl" readOnly="true">
                <query>
                    <![CDATA[select e from Country e order by e.name]]>
                </query>
            </loader>
        </collection>
        <collection id="cityDc" class="io.jmix.uisamples.entity.City">
            <fetchPlan extends="_base">
                <property name="country" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="cityDl" readOnly="true">
                <query>
                    <![CDATA[select e from City e where e.country = :country order by e.name]]>
                </query>
            </loader>
        </collection>
    </data>
    <content>
        <formLayout dataContainer="addressDc">
            <textField maxLength="32" property="zip"/>
            <entityComboBox id="countryComboBox" property="country" itemsContainer="countryDc"/>
            <entityComboBox id="cityComboBox" property="city" itemsContainer="cityDc"/>
            <textField property="addressLine"/>
        </formLayout>
    </content>
</fragment>




AddressFragment.java

package io.jmix.uisamples.view.flowui.fragments.data;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.component.combobox.EntityComboBox;
import io.jmix.flowui.component.formlayout.JmixFormLayout;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.Target;
import io.jmix.flowui.view.View;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.uisamples.entity.City;
import io.jmix.uisamples.entity.Country;

@FragmentDescriptor("address-fragment.xml")
public class AddressFragment extends Fragment<JmixFormLayout> {

    @ViewComponent
    protected EntityComboBox<City> cityComboBox;
    @ViewComponent
    protected CollectionLoader<Country> countryDl;
    @ViewComponent
    protected CollectionLoader<City> cityDl;

    @Subscribe(target = Target.HOST_CONTROLLER)
    public void onHostBeforeShow(View.BeforeShowEvent event) {
        countryDl.load();
    }

    @Subscribe(id = "countryDc", target = Target.DATA_CONTAINER)
    public void onCountryDcItemChange(final InstanceContainer.ItemChangeEvent<Country> event) {
        cityDl.setParameter("country", event.getItem());
        cityDl.load();
    }

    @Subscribe("countryComboBox")
    public void onCountryComboBoxValueChange(ComponentValueChangeEvent<EntityComboBox<Country>, Country> event) {
        if (event.isFromClient()) {
            cityComboBox.clear();
        }
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

