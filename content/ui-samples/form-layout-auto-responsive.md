<Path>Layouts > FormLayout > FormLayout with auto responsive</Path>

The auto responsive mode provides flexible configuration to make layout adapt smoothly to different screen sizes and device types. In this mode the responsiveSteps are ignored. Note that all available attributes for configuration are worked only when autoResponsive is enabled.

form-layout-auto-responsive.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <split height="100%" width="100%" splitterPosition="60">
            <formLayout id="formLayout" width="100%" classNames="p-m" autoResponsive="true">
                <formRow>
                    <formItem label="msg://firstName.label">
                        <textField/>
                    </formItem>
                    <formItem label="msg://lastName.label">
                        <textField/>
                    </formItem>
                    <formItem label="msg://rating.label">
                        <comboBox id="ratingField"/>
                    </formItem>
                </formRow>
                <formRow>
                    <formItem label="msg://countryName.label">
                        <textField/>
                    </formItem>
                    <formItem label="msg://birthDate.label">
                        <datePicker/>
                    </formItem>
                    <formItem label="msg://email.label">
                        <emailField/>
                    </formItem>
                </formRow>
                <formRow>
                    <formItem label="msg://status.label">
                        <comboBox/>
                    </formItem>
                    <formItem label="msg://phoneNumber.label">
                        <textField/>
                    </formItem>
                    <formItem label="msg://address.label">
                        <textField/>
                    </formItem>
                </formRow>
            </formLayout>

            <formLayout id="managementLayout" autoResponsive="true" autoRows="true"
                        classNames="p-m"
                        expandColumns="true"
                        expandFields="true"
                        rowSpacing="0">
                <vbox spacing="false" padding="false">
                    <textField id="columnSpacingField" placeholder="msg://columnSpacingField.placeholder"
                               datatype="string" label="msg://columnSpacingField.label" width="100%"/>
                    <textField id="rowSpacingField" placeholder="msg://rowSpacingField.placeholder" datatype="string"
                               label="msg://rowSpacingField.label" width="100%"/>
                    <textField id="labelSpacingField" placeholder="msg://labelSpacingField.placeholder"
                               datatype="string" label="msg://labelSpacingField.label" width="100%">
                        <suffix>
                            <button id="labelSpacingHelpButton" icon="INFO_CIRCLE" themeNames="tertiary-inline"/>
                        </suffix>
                    </textField>
                    <checkbox id="expandColumnsField" label="msg://expandColumnsField.label"/>
                    <checkbox id="expandFieldsField" label="msg://expandFieldsField.label"/>
                    <checkbox id="labelsAsideField" label="msg://labelsAsideField.label"/>
                </vbox>
                <vbox spacing="false" padding="false">
                    <integerField id="maxColumnsField" label="msg://maxColumnsField.label" width="100%" themeNames="align-center">
                        <prefix>
                            <button id="maxColumnsFieldMinus" icon="lumo:minus"/>
                        </prefix>
                        <suffix>
                            <button id="maxColumnsFieldPlus" icon="lumo:plus"/>
                        </suffix>
                    </integerField>
                    <integerField id="minColumnsField" label="msg://minColumnsField.label" width="100%" themeNames="align-center">
                        <prefix>
                            <button id="minColumnsFieldMinus" icon="lumo:minus"/>
                        </prefix>
                        <suffix>
                            <button id="minColumnsFieldPlus" icon="lumo:plus"/>
                        </suffix>
                    </integerField>
                </vbox>
            </formLayout>
        </split>
    </layout>
</view>




FormLayoutAutoResponsiveSample.java

package io.jmix.uisamples.view.flowui.containers.formlayout.autoresponsive;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.popover.Popover;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.formlayout.JmixFormLayout;
import io.jmix.flowui.component.textfield.JmixIntegerField;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;

import static io.jmix.core.common.util.Numbers.nullToZero;

@ViewController("form-layout-auto-responsive")
@ViewDescriptor("form-layout-auto-responsive.xml")
public class FormLayoutAutoResponsiveSample extends StandardView {

    @ViewComponent
    private JmixFormLayout formLayout;
    @ViewComponent
    private JmixIntegerField maxColumnsField;
    @ViewComponent
    private JmixIntegerField minColumnsField;

    @ViewComponent
    private MessageBundle messageBundle;

    @Subscribe
    public void onInit(final InitEvent event) {
        Popover popover = new Popover();
        popover.setFor("labelSpacingHelpButton");
        popover.add(new Span(messageBundle.getMessage("labelSpacingHelp")));
        getContent().add(popover);
    }

    @Subscribe("columnSpacingField")
    public void onColumnSpacingFieldComponentValueChange(final ComponentValueChangeEvent<TypedTextField<String>, String> event) {
        formLayout.setColumnSpacing(event.getValue());
    }

    @Subscribe("rowSpacingField")
    public void onRowSpacingFieldComponentValueChange(final ComponentValueChangeEvent<TypedTextField<String>, String> event) {
        formLayout.setRowSpacing(event.getValue());
    }

    @Subscribe("labelSpacingField")
    public void onLabelSpacingFieldComponentValueChange(final ComponentValueChangeEvent<TypedTextField<String>, String> event) {
        formLayout.setLabelSpacing(event.getValue());
    }

    @Subscribe("expandColumnsField")
    public void onExpandColumnsFieldComponentValueChange(final ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        formLayout.setExpandColumns(event.getValue());
    }

    @Subscribe("expandFieldsField")
    public void onExpandFieldsFieldComponentValueChange(final ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        formLayout.setExpandFields(event.getValue());
    }

    @Subscribe("labelsAsideField")
    public void onLabelsAsideFieldComponentValueChange(final ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        formLayout.setLabelsAside(event.getValue());
    }

    @Subscribe("maxColumnsField")
    public void onMaxColumnsFieldComponentValueChange(final ComponentValueChangeEvent<JmixIntegerField, Integer> event) {
        formLayout.setMaxColumns(nullToZero(event.getValue()));
    }

    @Subscribe("minColumnsField")
    public void onMinColumnsFieldComponentValueChange(final ComponentValueChangeEvent<JmixIntegerField, Integer> event) {
        formLayout.setMinColumns(nullToZero(event.getValue()));
    }

    @Subscribe(id = "maxColumnsFieldMinus", subject = "clickListener")
    public void onMaxColumnsFieldMinusClick(final ClickEvent<JmixButton> event) {
        maxColumnsField.setValue(nullToZero(maxColumnsField.getValue()) - 1);
    }

    @Subscribe(id = "maxColumnsFieldPlus", subject = "clickListener")
    public void onMaxColumnsFieldPlusClick(final ClickEvent<JmixButton> event) {
        maxColumnsField.setValue(nullToZero(maxColumnsField.getValue()) + 1);
    }

    @Subscribe(id = "minColumnsFieldMinus", subject = "clickListener")
    public void onMinColumnsFieldMinusClick(final ClickEvent<JmixButton> event) {
        minColumnsField.setValue(nullToZero(minColumnsField.getValue()) - 1);
    }

    @Subscribe(id = "minColumnsFieldPlus", subject = "clickListener")
    public void onMinColumnsFieldPlusClick(final ClickEvent<JmixButton> event) {
        minColumnsField.setValue(nullToZero(minColumnsField.getValue()) + 1);
    }
}


