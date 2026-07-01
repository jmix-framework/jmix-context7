<Path>Components > Tabs > Tabs with ThemeVariant</Path>

The Tabs component has several theme variants: small hide-scroll-buttons You can set these styles to the Tabs component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TabsVariant class.

tabs-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="tabs-theme-variant">
        <hbox padding="false" wrap="true">
            <checkboxGroup id="tabsSettingsCheckboxGroup" label="Tabs themes" themeNames="horizontal"/>
            <vbox padding="false" width="AUTO" justifyContent="END" classNames="tabs-count-control-box">
                <nativeLabel text="Tabs count" classNames="control-label"
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
import io.jmix.flowui.theme.StyleUtility;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

@ViewController("tabs-theme-variant")
@ViewDescriptor("tabs-theme-variant.xml")
public class TabsThemeVariantSample extends StandardView {

    @ViewComponent
    private Tabs tabs;
    @ViewComponent
    private JmixCheckboxGroup<String> tabsSettingsCheckboxGroup;
    @ViewComponent
    private HorizontalLayout controlButtonPlaceholder;

    @Autowired
    private UiComponents uiComponents;

    @Subscribe
    public void onInit(InitEvent event) {
        tabsSettingsCheckboxGroup.setItems(getTabsThemes());
        controlButtonPlaceholder.add(createRemoveTabButton(), createAddTabButton());
    }

    @Subscribe("tabsSettingsCheckboxGroup")
    public void onTabsSettingsCheckboxGroupValueChange(
            AbstractField.ComponentValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applyTabsThemes(event.getValue());
    }

    private void applyTabsThemes(Collection<String> themes) {
        tabs.getElement().getThemeList().clear();

        themes.stream()
                .map(String::toLowerCase)
                .forEach(tabs::addThemeName);
    }

    private Component createAddTabButton() {
        JmixButton button = uiComponents.create(JmixButton.class);
        button.setIcon(VaadinIcon.PLUS.create());
        button.addThemeVariants(ButtonVariant.LUMO_ICON);
        button.addClassName(StyleUtility.Button.LINK_BUTTON);

        button.addClickListener(event -> {
            long newTabIndex = tabs.getChildren().count() + 1;
            String tabLabel = "Tab " + newTabIndex;
            tabs.add(new Tab(tabLabel));
        });

        return button;
    }

    private Component createRemoveTabButton() {
        JmixButton button = uiComponents.create(JmixButton.class);
        button.setIcon(VaadinIcon.MINUS.create());
        button.addThemeVariants(ButtonVariant.LUMO_ICON);
        button.addClassName(StyleUtility.Button.LINK_BUTTON);

        button.addClickListener(event -> {
            long currentTabsSize = tabs.getChildren().count();
            if (currentTabsSize > 1) {
                Tab tabAt = tabs.getTabAt((int) (currentTabsSize - 1));
                tabs.remove(tabAt);
            }
        });

        return button;
    }

    private List<String> getTabsThemes() {
        return List.of("Small", "Hide-scroll-buttons");
    }
}




tabs-theme-variant.css


.tabs-theme-variant .tabs-count-control-box {
    gap: var(--vaadin-gap-s)
}

.tabs-theme-variant .control-label {
    font-size: var(--aura-font-size-s);
    font-weight: 500;
}

