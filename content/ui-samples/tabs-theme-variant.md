<Path>Components > Tabs > Tabs with ThemeVariant</Path>

The Tabs component has several theme variants: icon-on-top centered small minimal hide-scroll-buttons equal-width-tabs You can set these styles to the Tabs component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TabsVariant class.

tabs-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox padding="false" classNames="flex-wrap">
            <checkboxGroup id="tabsSettingsCheckboxGroup" label="Tabs themes"/>
            <vbox padding="false" width="AUTO" classNames="gap-s justify-end">
                <label text="Tabs count" classNames="text-secondary text-s font-medium"
                       setFor="controlButtonPlaceholder"/>
                <hbox id="controlButtonPlaceholder" padding="false"/>
            </vbox>
        </hbox>
        <tabs id="tabs" width="100%">
            <tab id="tab1" label="Tab 1"/>
            <tab id="tab2" label="Tab 2"/>
            <tab id="tab3" label="Tab 3"/>
            <tab id="tab4" label="Tab 4"/>
            <tab id="tab5" label="Tab 5"/>
            <tab id="tab6" label="Tab 6"/>
            <tab id="tab7" label="Tab 7"/>
            <tab id="tab8" label="Tab 8"/>
            <tab id="tab9" label="Tab 9"/>
            <tab id="tab10" label="Tab 10"/>
        </tabs>
        <span text="To make the scroll button appear, add or remove tabs using the corresponding buttons."/>
    </layout>
</view>




TabsThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.tabs.themevariant;

import com.vaadin.flow.component.AbstractField;
import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.tabs.Tab;
import com.vaadin.flow.component.tabs.Tabs;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Collection;
import java.util.List;

@ViewController("tabs-theme-variant")
@ViewDescriptor("tabs-theme-variant.xml")
public class TabsThemeVariantSample extends StandardView {

    @ViewComponent
    protected Tabs tabs;
    @ViewComponent
    protected JmixCheckboxGroup<String> tabsSettingsCheckboxGroup;
    @ViewComponent
    protected HorizontalLayout controlButtonPlaceholder;

    @Autowired
    protected UiComponents uiComponents;

    @Subscribe
    protected void onInit(InitEvent event) {
        List<String> tabsSettingsItems = List.of("Centered", "Small", "Minimal", "Hide-scroll-buttons",
                "Equal-width-tabs");
        tabsSettingsCheckboxGroup.setItems(tabsSettingsItems);

        controlButtonPlaceholder.add(createRemoveTabButton(), createAddTabButton());
    }

    @Subscribe("tabsSettingsCheckboxGroup")
    protected void onTabsSettingsCheckboxGroupValueChange(
            AbstractField.ComponentValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applyTabsThemes(event.getValue());
    }

    protected void applyTabsThemes(Collection<String> themes) {
        tabs.getElement().getThemeList().clear();

        themes.stream()
                .map(String::toLowerCase)
                .forEach(tabs::addThemeName);
    }

    protected Component createAddTabButton() {
        JmixButton button = uiComponents.create(JmixButton.class);
        button.setIcon(VaadinIcon.PLUS.create());
        button.addThemeVariants(ButtonVariant.LUMO_ICON, ButtonVariant.LUMO_TERTIARY_INLINE);

        button.addClickListener(event -> {
            long newTabIndex = tabs.getChildren().count() + 1;
            String tabLabel = "Tab " + newTabIndex;
            tabs.add(new Tab(tabLabel));
        });

        return button;
    }

    protected Component createRemoveTabButton() {
        JmixButton button = uiComponents.create(JmixButton.class);
        button.setIcon(VaadinIcon.MINUS.create());
        button.addThemeVariants(ButtonVariant.LUMO_ICON, ButtonVariant.LUMO_TERTIARY_INLINE);

        button.addClickListener(event -> {
            long currentTabsSize = tabs.getChildren().count();
            if (currentTabsSize > 1) {
                Tab tabAt = tabs.getTabAt((int) (currentTabsSize - 1));
                tabs.remove(tabAt);
            }
        });

        return button;
    }
}


