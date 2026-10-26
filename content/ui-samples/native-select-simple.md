<Path>Custom components > Native select > Native select with option groups</Path>

The sample integrates the native HTML `<select>` element with `<optgroup>` groups as the `NativeSelect` component. The browser draws the groups, handles the keyboard, and shows a native picker on mobile devices.

[`NativeSelect`]({currentPath}?tab=NativeSelect.java) extends `AbstractSinglePropertyField`: the `value` property of the element is synchronized with the server on the `change` event, and value change listeners work as for other fields. Its options are rendered as `<option>` and `<optgroup>` elements with the Element API, and their values are keys from a Vaadin `KeyMapper`: keys are never reused, so the server ignores a stale or unknown key. A native `<select>` has no label of its own, so the sample links a `nativeLabel` to it with the `setFor` attribute and styles it as a field label with the `native-select-label` class.

To declare the options and their groups in the view descriptor, the sample defines the [`native-select.xsd`]({currentPath}?tab=native-select.xsd) schema and the [`NativeSelectLoader`]({currentPath}?tab=NativeSelectLoader.java) loader, and registers the component with its loader in [`NativeSelectRegistration`]({currentPath}?tab=NativeSelectRegistration.java).


native-select-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:ns="http://io.jmix.uisamples/native-select.xsd">
    <layout>
        <vbox padding="false" spacing="false">
            <nativeLabel text="Dinosaur" setFor="dinosaurSelect" classNames="native-select-label"/>
            <ns:nativeSelect id="dinosaurSelect" width="15em">
                <ns:optgroup label="Theropods">
                    <ns:option value="tyrannosaurus" text="Tyrannosaurus"/>
                    <ns:option value="velociraptor" text="Velociraptor"/>
                    <ns:option value="deinonychus" text="Deinonychus"/>
                </ns:optgroup>
                <ns:optgroup label="Sauropods">
                    <ns:option value="diplodocus" text="Diplodocus"/>
                    <ns:option value="saltasaurus" text="Saltasaurus"/>
                    <ns:option value="apatosaurus" text="Apatosaurus"/>
                </ns:optgroup>
            </ns:nativeSelect>
        </vbox>
    </layout>
</view>




NativeSelectSimpleSample.java

package io.jmix.uisamples.view.flowui.customcomponents.nativeselect.simple;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.component.nativeselect.NativeSelect;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("native-select-simple")
@ViewDescriptor("native-select-simple.xml")
public class NativeSelectSimpleSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @Subscribe("dinosaurSelect")
    public void onDinosaurSelectComponentValueChange(
            final ComponentValueChangeEvent<NativeSelect<String>, String> event) {

        if (event.getValue() != null) {
            notifications.show("Selected value: " + event.getValue());
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




native-select.css


.native-select {
    --native-select-chevron: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230a0b0d' stroke-opacity='.65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='m6 9 6 6 6-6'/></svg>");
    appearance: none;
    padding: var(--vaadin-input-field-padding, var(--vaadin-padding-block-container) var(--vaadin-padding-inline-container));
    padding-inline-end: calc(var(--vaadin-padding-inline-container) + 1lh + var(--vaadin-gap-s));
    border: var(--vaadin-input-field-border-width, 1px) solid var(--vaadin-input-field-border-color, var(--vaadin-border-color));
    border-radius: var(--vaadin-input-field-border-radius, var(--vaadin-radius-m));
    background-color: var(--vaadin-input-field-background, var(--vaadin-background-color));
    background-image: var(--native-select-chevron);
    background-position: right calc(var(--vaadin-padding-inline-container) + 0.05lh) center;
    background-repeat: no-repeat;
    background-size: 0.9lh;
    box-shadow: var(--aura-shadow-xs);
    color: var(--vaadin-input-field-value-color, var(--vaadin-text-color));
    font: inherit;
    font-size: var(--vaadin-input-field-value-font-size, inherit);
    font-weight: var(--aura-font-weight-medium);
    cursor: var(--vaadin-clickable-cursor);
}

.native-select:focus-visible {
    outline: var(--vaadin-focus-ring-width) solid var(--vaadin-focus-ring-color);
    outline-offset: calc(var(--vaadin-input-field-border-width, 1px) * -1);
}

.native-select[readonly] {
    border-style: dashed;
    background-color: transparent;
    background-image: none;
    box-shadow: none;
    cursor: default;
}

.native-select:disabled {
    --native-select-chevron: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230a0b0d' stroke-opacity='.33' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='m6 9 6 6 6-6'/></svg>");
    border-color: transparent;
    background-color: var(--vaadin-input-field-disabled-background, var(--vaadin-background-container));
    box-shadow: none;
    color: var(--vaadin-input-field-disabled-text-color, var(--vaadin-text-color-disabled));
    cursor: default;
}

.native-select-label {
    margin-bottom: var(--vaadin-input-field-container-gap, var(--vaadin-gap-xs));
    color: var(--vaadin-input-field-label-color, var(--vaadin-text-color));
    font-size: var(--vaadin-input-field-label-font-size, inherit);
    font-weight: var(--vaadin-input-field-label-font-weight, 500);
    line-height: var(--vaadin-input-field-label-line-height, inherit);
}

[theme~='dark'] .native-select {
    --native-select-chevron: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23feffff' stroke-opacity='.65' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='m6 9 6 6 6-6'/></svg>");
}

[theme~='dark'] .native-select:disabled {
    --native-select-chevron: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23feffff' stroke-opacity='.33' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='m6 9 6 6 6-6'/></svg>");
}

@media (forced-colors: active) {
    .native-select {
        appearance: auto;
        background-image: none;
    }
}


