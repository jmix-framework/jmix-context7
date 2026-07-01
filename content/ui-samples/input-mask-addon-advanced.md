<Path>Custom components > Integrating Vaadin add-ons > Advanced Input Mask add-on</Path>

This sample demonstrates advanced integration of the `InputMask` component provided by the Vaadin addon.\
The basic integration can be found in [another sample]({contextPath}/sample/input-mask-addon-simple).

To fully implement the component in the Jmix UI, you need to perform the following steps:

1. Implement a composite component based on `TypedTextField` to wrap the `InputMask` functionality (see [`MaskField.java`]({currentPath}?tab=MaskField.java))
2. Create an XSD schema to support the component in XML descriptor (see [`mask-field.xsd`]({currentPath}?tab=mask-field.xsd))
3. Implement a component loader from XML (see [`MaskFieldLoader.java`]({currentPath}?tab=MaskFieldLoader.java))
4. Register the component and loader in the application (see [`MaskFieldRegistration.java`]({currentPath}?tab=MaskFieldRegistration.java))

After completing these steps, you will be able to use the component standardly in the Jmix UI.


input-mask-addon-advanced.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:mask="http://io.jmix.uisamples/mask.xsd">
    <layout>
        <mask:maskField id="phoneNumberField" label="msg://phoneNumberField.label"
                        helperText="msg://phoneNumberField.helperText" mask="+{1} 000 000-0000"
                        lazy="false" overwrite="true">

            <mask:suffix>
                <button id="showNumberBtn" icon="PHONE" classNames="link-button"/>
            </mask:suffix>
        </mask:maskField>
    </layout>
</view>




InputMaskAddonAdvancedSample.java

package io.jmix.uisamples.view.flowui.customcomponents.vaadinaddons.inputmaskadvanced;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.component.maskfield.MaskField;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("input-mask-addon-advanced")
@ViewDescriptor("input-mask-addon-advanced.xml")
public class InputMaskAddonAdvancedSample extends StandardView {

    @ViewComponent
    private MaskField phoneNumberField;

    @ViewComponent
    private MessageBundle messageBundle;

    @Autowired
    private Notifications notifications;

    @Subscribe("showNumberBtn")
    public void onShowNumberBtnClick(ClickEvent<JmixButton> event) {
        notifications.show(messageBundle.formatMessage("showNumberMessage", phoneNumberField.getValue()));
    }
}




MaskField.java

package io.jmix.uisamples.component.maskfield;

import com.vaadin.componentfactory.addons.inputmask.InputMask;
import com.vaadin.componentfactory.addons.inputmask.InputMaskOption;
import com.vaadin.flow.component.Composite;
import com.vaadin.flow.component.HasHelper;
import com.vaadin.flow.component.HasLabel;
import com.vaadin.flow.component.HasSize;
import com.vaadin.flow.component.shared.HasPrefix;
import com.vaadin.flow.component.shared.HasSuffix;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.textfield.TypedTextField;
import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class MaskField extends Composite<TypedTextField<String>>
        implements ApplicationContextAware, HasLabel, HasSize, HasHelper, HasSuffix, HasPrefix {

    private UiComponents uiComponents;
    private ApplicationContext applicationContext;

    private TypedTextField<String> root;

    private String mask;
    private InputMask inputMask;
    private List<InputMaskOption> options = Collections.emptyList();

    @Override
    protected TypedTextField<String> initContent() {
        root = uiComponents().create(TypedTextField.class);
        return root;
    }

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        this.applicationContext = applicationContext;
    }

    public void setMask(String mask) {
        if (inputMask != null) {
            inputMask.remove();
            this.mask = null;
        }

        inputMask = new InputMask(mask, options.toArray(new InputMaskOption[0]));
        this.mask = mask;
        inputMask.extend(root);
    }

    public void setOptions(List<InputMaskOption> options) {
        if (inputMask != null) {
            inputMask.remove();
        }

        inputMask = new InputMask(mask, options.toArray(new InputMaskOption[0]));
        this.options = options;
        inputMask.extend(root);
    }

    public void addOption(InputMaskOption option) {
        if (options.isEmpty()) {
            options = new ArrayList<>();
        }

        options.add(option);
        setOptions(options);
    }

    public String getValue() {
        return root.getTypedValue();
    }

    public void setValue(String value) {
        root.setTypedValue(value);
    }

    private UiComponents uiComponents() {
        if (uiComponents == null) {
            uiComponents = applicationContext.getBean(UiComponents.class);
        }

        return uiComponents;
    }
}




mask-field.xsd

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xs:schema xmlns="http://io.jmix.uisamples/mask.xsd"
           elementFormDefault="qualified"
           targetNamespace="http://io.jmix.uisamples/mask.xsd"
           xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:layout="http://jmix.io/schema/flowui/layout">

    <xs:element name="maskField">
        <xs:complexType>
            <xs:complexContent>
                <xs:extension base="layout:baseComponent">
                    <xs:sequence minOccurs="0">
                        <xs:element name="options" type="maskOptions"/>

                        <xs:element name="prefix" minOccurs="0" type="layout:prefixOrSuffixComponent"/>
                        <xs:element name="suffix" minOccurs="0" type="layout:prefixOrSuffixComponent"/>
                    </xs:sequence>

                    <xs:attribute name="mask" type="xs:string"/>
                    <xs:attribute name="label" type="layout:resourceString"/>
                    <xs:attribute name="helperText" type="layout:resourceString"/>

                    <xs:attribute name="lazy" type="xs:boolean"/>
                    <xs:attribute name="overwrite" type="xs:boolean"/>
                    <xs:attribute name="uppercase" type="xs:boolean"/>

                    <xs:attributeGroup ref="layout:hasSize"/>
                </xs:extension>
            </xs:complexContent>
        </xs:complexType>
    </xs:element>

    <xs:complexType name="maskOptions">
        <xs:sequence maxOccurs="unbounded" minOccurs="0">
            <xs:element name="option">
                <xs:complexType>
                    <xs:sequence maxOccurs="unbounded" minOccurs="0">
                        <xs:element name="options" type="maskOptions"/>
                    </xs:sequence>

                    <xs:attribute name="key" type="maskOptionKeyType"/>
                    <xs:attribute name="value" type="xs:string"/>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>

    <xs:simpleType name="maskOptionKeyType">
        <xs:union>
            <xs:simpleType>
                <xs:restriction base="xs:string"/>
            </xs:simpleType>
            <xs:simpleType>
                <xs:restriction base="xs:string">
                    <xs:enumeration value="lazy"/>
                    <xs:enumeration value="overwrite"/>
                    <xs:enumeration value="blocks"/>
                </xs:restriction>
            </xs:simpleType>
        </xs:union>
    </xs:simpleType>

</xs:schema>




MaskFieldLoader.java

package io.jmix.uisamples.component.maskfield;

import com.vaadin.componentfactory.addons.inputmask.InputMaskOption;
import io.jmix.flowui.xml.layout.loader.AbstractComponentLoader;
import io.jmix.flowui.xml.layout.support.PrefixSuffixLoaderSupport;
import org.dom4j.Element;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

public class MaskFieldLoader extends AbstractComponentLoader<MaskField> {

    protected PrefixSuffixLoaderSupport prefixSuffixLoaderSupport;

    @Override
    protected MaskField createComponent() {
        return factory.create(MaskField.class);
    }

    @Override
    public void initComponent() {
        super.initComponent();

        prefixSuffixLoaderSupport().createPrefixSuffixComponents(resultComponent, element);
    }

    @Override
    public void loadComponent() {
        loadResourceString(element, "label", context.getMessageGroup(), resultComponent::setLabel);
        loadString(element, "mask", resultComponent::setMask);

        componentLoader().loadSizeAttributes(resultComponent, element);
        componentLoader().loadHelperText(resultComponent, element);
        prefixSuffixLoaderSupport().loadPrefixSuffixComponents();

        loadOptions(resultComponent::setOptions, element);
        loadDefaultOptions(resultComponent, element);
    }

    private void loadDefaultOptions(MaskField resultComponent, Element element) {
        loadBoolean(element, "lazy")
                .map(InputMaskOption::lazy)
                .ifPresent(resultComponent::addOption);

        loadBoolean(element, "overwrite")
                .map(InputMaskOption::overwrite)
                .ifPresent(resultComponent::addOption);
    }

    private void loadOptions(Consumer<List<InputMaskOption>> setter, Element element) {
        Element optionsElement = element.element("options");
        if (optionsElement == null) {
            return;
        }

        ArrayList<InputMaskOption> optionsList = new ArrayList<>();
        for (Element option : optionsElement.elements("option")) {
            optionsList.add(loadOption(option));
        }

        setter.accept(optionsList);
    }

    private InputMaskOption loadOption(Element element) {
        String key = element.attributeValue("key");

        List<InputMaskOption> options = new ArrayList<>();
        loadOptions(options::addAll, element);

        if (!options.isEmpty()) {
            return InputMaskOption.option(key, options);
        }

        String value = element.attributeValue("value");
        return InputMaskOption.option(key, value);
    }

    private PrefixSuffixLoaderSupport prefixSuffixLoaderSupport() {
        if (prefixSuffixLoaderSupport == null) {
            prefixSuffixLoaderSupport = applicationContext.getBean(PrefixSuffixLoaderSupport.class, context);
        }
        return prefixSuffixLoaderSupport;
    }
}




MaskFieldRegistration.java

package io.jmix.uisamples.view.flowui.customcomponents.vaadinaddons.inputmaskadvanced;

import io.jmix.flowui.sys.registration.ComponentRegistration;
import io.jmix.flowui.sys.registration.ComponentRegistrationBuilder;
import io.jmix.uisamples.component.maskfield.MaskField;
import io.jmix.uisamples.component.maskfield.MaskFieldLoader;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MaskFieldRegistration {

    @Bean
    public ComponentRegistration maskField() {
        return ComponentRegistrationBuilder.create(MaskField.class)
                .withComponentLoader("maskField", MaskFieldLoader.class)
                .build();
    }
}


