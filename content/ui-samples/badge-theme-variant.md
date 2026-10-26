<Path>Components > Badge > Badge with ThemeVariant</Path>

`Badge` has the following theme variants:

- `success`, `warning`, `error` – color
- `small` – a smaller badge
- `filled` – a solid fill instead of a tinted surface
- `dot` – renders the badge as a small dot indicator and visually hides all its content
- `icon-only`, `number-only` – visually hide everything but the icon or the number, keeping the text for screen readers


Apply variants with the `themeNames` attribute in the XML descriptor, or with `addThemeVariants(BadgeVariant…)` in the view controller.


badge-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="horizontal-layout">
        <vbox width="AUTO" padding="false">
            <details summaryText="Style variant" opened="true">
                <hbox wrap="true">
                    <badge id="defaultBadge" text="Default badge"/>
                    <badge id="successBadge" text="Success badge" themeNames="success"/>
                    <badge id="warningBadge" text="Warning badge" themeNames="warning"/>
                    <badge id="errorBadge" text="Error badge" themeNames="error"/>
                </hbox>
            </details>

            <details summaryText="Size variant" opened="true">
                <hbox wrap="true">
                    <badge id="mediumBadge" text="Medium badge"/>
                    <badge id="smallBadge" text="Small badge" themeNames="small"/>
                </hbox>
            </details>

            <details summaryText="Visual variant" opened="true">
                <hbox wrap="true" alignItems="CENTER">
                    <badge id="filledBadge" text="Filled badge" themeNames="filled"/>
                    <badge id="iconOnlyBadge" text="Confirmed" icon="CHECK" themeNames="icon-only"/>
                    <badge id="numberOnlyBadge" text="unread messages" number="5" themeNames="number-only"/>
                    <badge id="dotBadge" text="Online" themeNames="dot"/>
                </hbox>
            </details>
        </vbox>
        <details summaryText="Test badge" opened="true" width="35%">
            <vbox padding="false">
                <badge id="testBadge"/>
                <checkboxGroup id="settingsCheckboxGroup" label="TestBadge settings" themeNames="vertical"/>
            </vbox>
        </details>
    </layout>
</view>




BadgeThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.badge.themevariant;

import com.vaadin.flow.component.badge.Badge;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.icon.Icons;
import io.jmix.flowui.kit.icon.JmixFontIcon;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Collection;
import java.util.List;

@ViewController("badge-theme-variant")
@ViewDescriptor("badge-theme-variant.xml")
public class BadgeThemeVariantSample extends StandardView {

    @ViewComponent
    protected Badge testBadge;
    @ViewComponent
    protected JmixCheckboxGroup<String> settingsCheckboxGroup;
    @Autowired
    private Icons icons;

    @Subscribe
    protected void onInit(InitEvent event) {
        settingsCheckboxGroup.setItems(getSettingsCheckboxGroupItems());
    }

    @Subscribe("settingsCheckboxGroup")
    protected void onSettingsValueChange(TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        //clear
        testBadge.setText(null);
        testBadge.setNumber(null);
        testBadge.setIcon(null);
        testBadge.getElement().getThemeList().clear();

        event.getValue().stream()
                .map(String::toLowerCase)
                .forEach(this::applyTestBadgeSetting);
    }

    protected void applyTestBadgeSetting(String setting) {
        switch (setting) {
            case "text" -> testBadge.setText("Badge text");
            case "number" -> testBadge.setNumber(5);
            case "icon" -> testBadge.setIcon(icons.get(JmixFontIcon.SMILEY));
            default -> testBadge.getElement().getThemeList().add(setting);
        }
    }

    protected List<String> getSettingsCheckboxGroupItems() {
        return List.of("Text", "Number", "Icon", "Success", "Warning", "Error",
                "Filled", "Small", "Dot", "Icon-only", "Number-only");
    }
}


