<Path>Layouts > TabSheet > TabSheet with ThemeVariant</Path>

The TabSheet component has several theme variants: icon-on-top centered small minimal hide-scroll-buttons equal-width-tabs bordered You can set these styles to the TabSheet component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TabSheetVariant class.

tabsheet-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <checkboxGroup id="tabSheetSettingsCheckboxGroup" label="TabSheet themes"/>
        <tabSheet id="tabSheet" width="100%">
            <tab id="tab1" label="Tab 1">
                <div/>
            </tab>
            <tab id="tab2" label="Tab 2">
                <div/>
            </tab>
            <tab id="tab3" label="Tab 3">
                <div/>
            </tab>
            <tab id="tab4" label="Tab 4">
                <div/>
            </tab>
            <tab id="tab5" label="Tab 5">
                <div/>
            </tab>
            <tab id="tab6" label="Tab 6">
                <div/>
            </tab>
            <tab id="tab7" label="Tab 7">
                <div/>
            </tab>
            <tab id="tab8" label="Tab 8">
                <div/>
            </tab>
            <tab id="tab9" label="Tab 9">
                <div/>
            </tab>
            <tab id="tab10" label="Tab 10">
                <div/>
            </tab>
        </tabSheet>
        <span text="To make the scroll button appear, add or remove tabs using the corresponding buttons."/>
    </layout>
</view>




TabSheetThemeVariantSample.java

package io.jmix.uisamples.view.flowui.containers.tabsheet.themevariant;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.icon.VaadinIcon;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.component.tabsheet.JmixTabSheet;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Collection;
import java.util.List;

@ViewController("tabsheet-theme-variant")
@ViewDescriptor("tabsheet-theme-variant.xml")
public class TabSheetThemeVariantSample extends StandardView {

    @ViewComponent
    protected JmixTabSheet tabSheet;
    @ViewComponent
    protected JmixCheckboxGroup<String> tabSheetSettingsCheckboxGroup;

    @Autowired
    protected UiComponents uiComponents;

    @Subscribe
    protected void onInit(InitEvent event) {
        List<String> tabSheetSettingsItems = List.of("Centered", "Small", "Minimal", "Hide-scroll-buttons",
                "Equal-width-tabs", "Bordered");
        tabSheetSettingsCheckboxGroup.setItems(tabSheetSettingsItems);

        tabSheet.setSuffixComponent(createAddTabButton());
        tabSheet.setPrefixComponent(createRemoveTabButton());
    }

    @Subscribe("tabSheetSettingsCheckboxGroup")
    protected void onTabSheetSettingsCheckboxGroupValueChange(
            ComponentValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applyTabSheetThemes(event.getValue());
    }

    protected void applyTabSheetThemes(Collection<String> themes) {
        tabSheet.getElement().getThemeList().clear();

        themes.stream()
                .map(String::toLowerCase)
                .forEach(tabSheet::addThemeName);
    }

    protected Component createAddTabButton() {
        JmixButton button = uiComponents.create(JmixButton.class);
        button.setIcon(VaadinIcon.PLUS.create());
        button.addThemeVariants(ButtonVariant.LUMO_ICON, ButtonVariant.LUMO_TERTIARY_INLINE);

        button.addClickListener(event -> {
            int newTabIndex = tabSheet.getOwnComponents().size() + 1;
            String tabLabel = "Tab " + newTabIndex;
            tabSheet.add(tabLabel, new Div());
        });

        return button;
    }

    protected Component createRemoveTabButton() {
        JmixButton button = uiComponents.create(JmixButton.class);
        button.setIcon(VaadinIcon.MINUS.create());
        button.addThemeVariants(ButtonVariant.LUMO_ICON, ButtonVariant.LUMO_TERTIARY_INLINE);

        button.addClickListener(event -> {
            int currentTabSheetSize = tabSheet.getOwnComponents().size();
            if (currentTabSheetSize > 1) {
                tabSheet.remove(currentTabSheetSize - 1);
            }
        });

        return button;
    }
}


