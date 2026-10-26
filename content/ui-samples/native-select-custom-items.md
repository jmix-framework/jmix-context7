<Path>Custom components > Native select > Native select with custom items</Path>

Items of [`NativeSelect`]({currentPath}?tab=NativeSelect.java) can be any objects, not only strings. The component implements `SupportsItemsContainer`, so the sample passes the `citiesDc` container in the `itemsContainer` attribute, and the options follow the container changes. `setItemLabelGenerator()` defines the text of each option, and `setGroupLabelGenerator()` defines the `<optgroup>` it belongs to, so the cities are grouped by country. The value of the component is the selected `City` instance.


native-select-custom-items.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:ns="http://io.jmix.uisamples/native-select.xsd">
    <data>
        <collection id="citiesDc"
                    class="io.jmix.uisamples.entity.City">
            <fetchPlan extends="_base">
                <property name="country" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="citiesDl">
                <query>
                    <![CDATA[select e from City e order by e.country.name, e.name]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <vbox padding="false" spacing="false">
            <nativeLabel text="City" setFor="citySelect" classNames="native-select-label"/>
            <ns:nativeSelect id="citySelect" itemsContainer="citiesDc" width="15em"/>
        </vbox>
    </layout>
</view>




NativeSelectCustomItemsSample.java

package io.jmix.uisamples.view.flowui.customcomponents.nativeselect.customitems;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.component.nativeselect.NativeSelect;
import io.jmix.uisamples.entity.City;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("native-select-custom-items")
@ViewDescriptor("native-select-custom-items.xml")
public class NativeSelectCustomItemsSample extends StandardView {

    @ViewComponent
    private NativeSelect<City> citySelect;

    @Autowired
    private Notifications notifications;

    @Subscribe
    public void onInit(final InitEvent event) {
        citySelect.setItemLabelGenerator(City::getName);
        citySelect.setGroupLabelGenerator(city -> city.getCountry().getName());
    }

    @Subscribe("citySelect")
    public void onCitySelectComponentValueChange(final ComponentValueChangeEvent<NativeSelect<City>, City> event) {
        City city = event.getValue();
        if (city != null) {
            notifications.show("Selected city: %s, %s".formatted(city.getName(), city.getCountry().getName()));
        }
    }
}




NativeSelect.java

package io.jmix.uisamples.component.nativeselect;

import com.vaadin.flow.component.AbstractSinglePropertyField;
import com.vaadin.flow.component.Focusable;
import com.vaadin.flow.component.HasAriaLabel;
import com.vaadin.flow.component.HasSize;
import com.vaadin.flow.component.ItemLabelGenerator;
import com.vaadin.flow.component.Tag;
import com.vaadin.flow.data.provider.KeyMapper;
import com.vaadin.flow.dom.Element;
import com.vaadin.flow.shared.Registration;
import io.jmix.core.common.event.Subscription;
import io.jmix.flowui.data.SupportsItemsContainer;
import io.jmix.flowui.data.SupportsValueSource;
import io.jmix.flowui.data.ValueSource;
import io.jmix.flowui.data.binding.impl.AbstractValueBinding;
import io.jmix.flowui.data.binding.impl.FieldValueBinding;
import io.jmix.flowui.model.CollectionContainer;
import org.jspecify.annotations.Nullable;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

@Tag("select")
public class NativeSelect<V> extends AbstractSinglePropertyField<NativeSelect<V>, V>
        implements HasSize, HasAriaLabel, Focusable<NativeSelect<V>>, SupportsValueSource<V>,
        SupportsItemsContainer<V>, ApplicationContextAware {

    private static final String EMPTY_KEY = "";

    @Nullable
    private ApplicationContext applicationContext;

    private final KeyMapper<V> keyMapper = new KeyMapper<>();
    private List<V> items = List.of();

    private ItemLabelGenerator<V> itemLabelGenerator = String::valueOf;
    @Nullable
    private ItemLabelGenerator<V> groupLabelGenerator;

    @Nullable
    private AbstractValueBinding<V> valueBinding;
    @Nullable
    private Registration itemsContainerRegistration;
    private boolean updatingPresentation;

    public NativeSelect() {
        super("value", null, String.class, NativeSelect::toItem, NativeSelect::toKey);

        setSynchronizedEvent("change");
        addClassName("native-select");

        renderOptions();
    }

    public List<V> getItems() {
        return items;
    }

    public void setItems(Collection<V> items) {
        this.items = List.copyOf(items);
        keyMapper.removeAll();
        renderOptions();
    }

    @Override
    public void setItems(CollectionContainer<V> container) {
        if (itemsContainerRegistration != null) {
            itemsContainerRegistration.remove();
        }

        Subscription collectionChange = container.addCollectionChangeListener(event -> setItems(container.getItems()));
        Subscription itemPropertyChange = container.addItemPropertyChangeListener(event -> renderOptions());
        itemsContainerRegistration = Registration.combine(collectionChange::remove, itemPropertyChange::remove);

        setItems(container.getItems());
    }

    public void setItemLabelGenerator(ItemLabelGenerator<V> itemLabelGenerator) {
        this.itemLabelGenerator = itemLabelGenerator;
        renderOptions();
    }

    public void setGroupLabelGenerator(@Nullable ItemLabelGenerator<V> groupLabelGenerator) {
        this.groupLabelGenerator = groupLabelGenerator;
        renderOptions();
    }

    @Override
    public void setReadOnly(boolean readOnly) {
        super.setReadOnly(readOnly);
        getElement().setAttribute("readonly", readOnly);

        renderOptions();
    }

    @Override
    public void setRequiredIndicatorVisible(boolean requiredIndicatorVisible) {
        super.setRequiredIndicatorVisible(requiredIndicatorVisible);
        renderOptions();
    }

    @Nullable
    @Override
    public ValueSource<V> getValueSource() {
        return valueBinding != null ? valueBinding.getValueSource() : null;
    }

    @Override
    public void setValueSource(@Nullable ValueSource<V> valueSource) {
        if (valueBinding != null) {
            valueBinding.unbind();
            valueBinding = null;
        }

        if (valueSource != null) {
            valueBinding = createValueBinding(valueSource);
            valueBinding.bind();
            valueBinding.activate();
        }
    }

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) {
        this.applicationContext = applicationContext;
    }

    @SuppressWarnings("unchecked")
    protected AbstractValueBinding<V> createValueBinding(ValueSource<V> valueSource) {
        return Objects.requireNonNull(applicationContext)
                .getBean(FieldValueBinding.class, valueSource, this);
    }

    @Override
    protected void setPresentationValue(@Nullable V value) {
        updatingPresentation = true;
        try {
            super.setPresentationValue(value);
        } finally {
            updatingPresentation = false;
        }
    }

    @Override
    protected boolean hasValidValue() {
        String key = getElement().getProperty("value", EMPTY_KEY);
        return !updatingPresentation && (key.isEmpty() || keyMapper.containsKey(key));
    }

    protected void renderOptions() {
        items.forEach(keyMapper::key);
        String selectedKey = toKey(getValue());

        getElement().removeAllChildren();
        getElement().appendChild(createOption(EMPTY_KEY, "", selectedKey));

        Map<String, Element> groups = new HashMap<>();
        for (V item : items) {
            Element option = createOption(keyMapper.key(item), itemLabelGenerator.apply(item), selectedKey);

            String groupLabel = groupLabelGenerator != null ? groupLabelGenerator.apply(item) : null;
            if (groupLabel != null) {
                groups.computeIfAbsent(groupLabel, this::createGroup).appendChild(option);
            } else {
                getElement().appendChild(option);
            }
        }

        setPresentationValue(getValue());
    }

    protected Element createGroup(String label) {
        Element group = new Element("optgroup").setAttribute("label", label);
        getElement().appendChild(group);
        return group;
    }

    protected Element createOption(String key, String label, String selectedKey) {
        return new Element("option")
                .setAttribute("value", key)
                .setAttribute("selected", key.equals(selectedKey))
                .setAttribute("disabled", isReadOnly() || key.isEmpty() && isRequiredIndicatorVisible())
                .setText(label);
    }

    @Nullable
    protected V toItem(String key) {
        return keyMapper.get(key);
    }

    protected String toKey(@Nullable V item) {
        return item != null && keyMapper.has(item) ? keyMapper.key(item) : EMPTY_KEY;
    }
}




native-select.xsd

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xs:schema xmlns="http://io.jmix.uisamples/native-select.xsd"
           elementFormDefault="qualified"
           targetNamespace="http://io.jmix.uisamples/native-select.xsd"
           xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:layout="http://jmix.io/schema/flowui/layout">

    <xs:element name="nativeSelect">
        <xs:complexType>
            <xs:complexContent>
                <xs:extension base="layout:baseComponent">
                    <xs:choice minOccurs="0" maxOccurs="unbounded">
                        <xs:element name="optgroup" type="optgroupType"/>
                        <xs:element name="option" type="optionType"/>
                    </xs:choice>

                    <xs:attribute name="itemsContainer" type="xs:string"/>
                    <xs:attributeGroup ref="layout:hasSize"/>
                    <xs:attributeGroup ref="layout:hasClassNames"/>
                    <xs:attributeGroup ref="layout:hasEnabled"/>
                    <xs:attributeGroup ref="layout:hasAriaLabel"/>
                    <xs:attributeGroup ref="layout:hasDataContainer"/>
                </xs:extension>
            </xs:complexContent>
        </xs:complexType>
    </xs:element>

    <xs:complexType name="optgroupType">
        <xs:sequence>
            <xs:element name="option" type="optionType" maxOccurs="unbounded"/>
        </xs:sequence>
        <xs:attribute name="label" type="layout:resourceString" use="required"/>
    </xs:complexType>

    <xs:complexType name="optionType">
        <xs:attribute name="value" type="xs:string" use="required"/>
        <xs:attribute name="text" type="layout:resourceString"/>
    </xs:complexType>

</xs:schema>




NativeSelectLoader.java

package io.jmix.uisamples.component.nativeselect;

import io.jmix.flowui.data.ValueSource;
import io.jmix.flowui.exception.GuiDevelopmentException;
import io.jmix.flowui.xml.layout.loader.AbstractComponentLoader;
import io.jmix.flowui.xml.layout.support.DataLoaderSupport;
import org.dom4j.Element;

import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

public class NativeSelectLoader extends AbstractComponentLoader<NativeSelect<String>> {

    @SuppressWarnings("unchecked")
    @Override
    protected NativeSelect<String> createComponent() {
        return factory.create(NativeSelect.class);
    }

    @Override
    public void loadComponent() {
        componentLoader().loadSizeAttributes(resultComponent, element);
        componentLoader().loadClassNames(resultComponent, element);
        componentLoader().loadEnabled(resultComponent, element);
        componentLoader().loadAriaLabel(resultComponent, element);

        boolean hasOptions = loadOptions();
        if (hasOptions && element.attribute("itemsContainer") != null) {
            throw new GuiDevelopmentException("'nativeSelect' can't have both options and 'itemsContainer'", context);
        }

        DataLoaderSupport dataLoaderSupport = applicationContext.getBean(DataLoaderSupport.class, context);
        dataLoaderSupport.loadItems(resultComponent, element);
        dataLoaderSupport.loadData(resultComponent, element);

        ValueSource<String> valueSource = resultComponent.getValueSource();
        if (hasOptions && valueSource != null && valueSource.getType() != String.class) {
            throw new GuiDevelopmentException("Options declared in XML can be bound only to a String property",
                    context, "property", element.attributeValue("property"));
        }
    }

    protected boolean loadOptions() {
        Map<String, String> labels = new LinkedHashMap<>();
        Map<String, String> groups = new HashMap<>();
        Set<String> groupLabels = new HashSet<>();

        for (Element child : element.elements()) {
            if ("optgroup".equals(child.getName())) {
                String groupLabel = loadResourceString(child, "label", context.getMessageGroup())
                        .orElseThrow(() -> new GuiDevelopmentException("'optgroup' requires a 'label'", context));
                if (!groupLabels.add(groupLabel)) {
                    throw new GuiDevelopmentException("Duplicate 'optgroup' label", context, "label", groupLabel);
                }

                for (Element option : child.elements("option")) {
                    groups.put(loadOption(option, labels), groupLabel);
                }
            } else if ("option".equals(child.getName())) {
                loadOption(child, labels);
            }
        }

        if (labels.isEmpty()) {
            return false;
        }

        resultComponent.setItemLabelGenerator(value -> labels.getOrDefault(value, value));
        resultComponent.setGroupLabelGenerator(groups::get);
        resultComponent.setItems(labels.keySet());
        return true;
    }

    protected String loadOption(Element option, Map<String, String> labels) {
        String value = loadString(option, "value")
                .orElseThrow(() -> new GuiDevelopmentException("'option' requires a non-empty 'value'", context));
        if (labels.containsKey(value)) {
            throw new GuiDevelopmentException("Duplicate 'option' value", context, "value", value);
        }

        labels.put(value, loadResourceString(option, "text", context.getMessageGroup()).orElse(value));
        return value;
    }
}




NativeSelectRegistration.java

package io.jmix.uisamples.view.flowui.customcomponents.nativeselect;

import io.jmix.flowui.sys.registration.ComponentRegistration;
import io.jmix.flowui.sys.registration.ComponentRegistrationBuilder;
import io.jmix.uisamples.component.nativeselect.NativeSelect;
import io.jmix.uisamples.component.nativeselect.NativeSelectLoader;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class NativeSelectRegistration {

    @Bean
    public ComponentRegistration nativeSelect() {
        return ComponentRegistrationBuilder.create(NativeSelect.class)
                .withComponentLoader("nativeSelect", NativeSelectLoader.class)
                .build();
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

