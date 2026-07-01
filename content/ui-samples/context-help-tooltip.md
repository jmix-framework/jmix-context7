<Path>Components > ContextHelp > Tooltip</Path>

A tooltip is a customizable context tooltip. Attributes: focusDelay - the delay in milliseconds before the tooltip is opened on keyboard focus, when not in manual mode. hideDelay - the delay in milliseconds before the tooltip is closed on losing hover, when not in manual mode. On blur, the tooltip is closed immediately. hoverDelay - the delay in milliseconds before the tooltip is opened on hover, when not in manual mode. manual - when true, the tooltip is controlled programmatically instead of reacting to focus and mouse events. position - position of the tooltip with respect to its target. text - the string used as a tooltip content.

context-help-tooltip.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Default tooltip" opened="true" width="AUTO">
            <hbox wrap="true">
                <textField label="Field with tooltip">
                    <tooltip text="Tooltip text"/>
                </textField>
                <textField id="manualTooltipField" label="Manual tooltip">
                    <tooltip text="Tooltip text" manual="true" position="END_BOTTOM"/>
                </textField>
            </hbox>
        </details>
        <details summaryText="Custom tooltip" opened="true" width="AUTO">
            <vbox padding="false">
                <textField id="customTooltipField" placeholder="Field for a tooltip">
                    <tooltip text="Tooltip text"/>
                </textField>
                <formLayout>
                    <responsiveSteps>
                        <responsiveStep minWidth="0" columns="1"/>
                        <responsiveStep minWidth="25em" columns="2"/>
                    </responsiveSteps>
                    <integerField id="focusDelay" label="FocusDelay">
                        <validators>
                            <min value="0"/>
                            <max value="5000"/>
                        </validators>
                    </integerField>
                    <integerField id="hideDelay" min="1" max="5" label="HideDelay">
                        <validators>
                            <min value="0"/>
                            <max value="5000"/>
                        </validators>
                    </integerField>
                    <integerField id="hoverDelay" min="1" max="5" label="HoverDelay">
                        <validators>
                            <min value="0"/>
                            <max value="5000"/>
                        </validators>
                    </integerField>
                    <checkbox id="manual" label="Manual"/>
                    <select id="position" label="Position"/>
                    <textField id="text" value="Tooltip text" label="Text"/>
                </formLayout>
            </vbox>
        </details>
    </layout>
</view>




ContextHelpTooltipSample.java

package io.jmix.uisamples.view.flowui.components.contexthelp.tooltip;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.shared.Tooltip;
import com.vaadin.flow.component.textfield.IntegerField;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.SupportsTypedValue;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.select.JmixSelect;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.theme.StyleUtility;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Arrays;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@ViewController("context-help-tooltip")
@ViewDescriptor("context-help-tooltip.xml")
public class ContextHelpTooltipSample extends StandardView {

    @ViewComponent
    protected TypedTextField<String> manualTooltipField;
    @ViewComponent
    protected TypedTextField<String> customTooltipField;
    @ViewComponent
    protected JmixSelect<Tooltip.TooltipPosition> position;

    @Autowired
    protected UiComponents uiComponents;

    @Subscribe
    protected void onInit(InitEvent event) {
        initManualTooltip();
        initPositionItems();
    }

    protected void initManualTooltip() {
        JmixButton helperButton = createHelperButton();
        Tooltip tooltip = manualTooltipField.getTooltip();
        helperButton.addClickListener(e -> tooltip.setOpened(!tooltip.isOpened()));

        manualTooltipField.setSuffixComponent(helperButton);
    }

    protected void initPositionItems() {
        ComponentUtils.setItemsMap(position, getPositionItemsMap());
        position.setValue(Tooltip.TooltipPosition.TOP);
    }

    @Subscribe("focusDelay")
    protected void onFocusDelayChange(ComponentValueChangeEvent<IntegerField, Integer> event) {
        Integer value = event.getValue();

        if (value != null && value > 0 && value <= 5000) {
            customTooltipField.getTooltip().setFocusDelay(value);
        } else {
            customTooltipField.getTooltip().setFocusDelay(0);
        }
    }

    @Subscribe("hideDelay")
    protected void onHideDelayChange(ComponentValueChangeEvent<IntegerField, Integer> event) {
        Integer value = event.getValue();

        if (value != null && value > 0 && value <= 5000) {
            customTooltipField.getTooltip().setHideDelay(value);
        } else {
            customTooltipField.getTooltip().setHideDelay(0);
        }
    }

    @Subscribe("hoverDelay")
    protected void onHoverDelayChange(ComponentValueChangeEvent<IntegerField, Integer> event) {
        Integer value = event.getValue();

        if (value != null && value > 0 && value <= 5000) {
            customTooltipField.getTooltip().setHoverDelay(value);
        } else {
            customTooltipField.getTooltip().setHoverDelay(0);
        }
    }

    @Subscribe("manual")
    protected void onManualChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        Tooltip tooltip = customTooltipField.getTooltip();
        tooltip.setManual(event.getValue());

        if (event.getValue()) {
            JmixButton helperButton = createHelperButton();
            helperButton.addClickListener(e -> tooltip.setOpened(!tooltip.isOpened()));

            customTooltipField.setSuffixComponent(helperButton);
        } else {
            customTooltipField.setSuffixComponent(null);
        }
    }

    @Subscribe("position")
    protected void onPositionChange(
            ComponentValueChangeEvent<JmixSelect<Tooltip.TooltipPosition>, Tooltip.TooltipPosition> event) {
        customTooltipField.getTooltip().setPosition(event.getValue());
    }

    @Subscribe("text")
    protected void onTextChange(SupportsTypedValue.TypedValueChangeEvent<TypedTextField<String>, String> event) {
        customTooltipField.getTooltip().setText(event.getValue());
    }

    protected JmixButton createHelperButton() {
        JmixButton helperButton = uiComponents.create(JmixButton.class);
        helperButton.setIcon(VaadinIcon.QUESTION_CIRCLE.create());
        helperButton.addThemeVariants(ButtonVariant.LUMO_ICON);
        helperButton.addClassName(StyleUtility.Button.LINK_BUTTON);

        return helperButton;
    }

    protected Map<Tooltip.TooltipPosition, String> getPositionItemsMap() {
        return Arrays.stream(Tooltip.TooltipPosition.values())
                .collect(Collectors.toMap(Function.identity(),mode -> mode.name().replace('_', ' ')));
    }
}


