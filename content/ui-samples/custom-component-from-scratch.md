<Path>Custom components > Creating component from scratch</Path>

This example shows how to build the light/dark theme toggle.

The server-side part of the component is located in [`ThemeToggle.java`]({currentPath}?tab=ThemeToggle.java). It
contains a number of annotations for integration with the client-side part:

- `@Tag` – specifies the name of the custom HTML element of the web component
- `@JsModule` – imports the JavaScript module containing the client-side part of the component

Client-side events sent as `CustomEvent` JavaScript objects are declared on the server side using the `@DomEvent` and
`@EventData` annotations. Also, the component class has a listener registration method for these events. See
`ThemeToggleThemeChangedEvent` nested class and `addThemeChangeListener()` method in [
`ThemeToggle.java`]({currentPath}?tab=ThemeToggle.java).

The [`theme-toggle.js`]({currentPath}?tab=theme-toggle.js) file located in the `frontend/src/component/theme-switcher`
folder contains the client-side part, which is a web component extending Vaadin's `Button`.

After creating the client-side and server-side parts of the component, it can be used in views by creating an instance
of its Java class and adding it to a parent component.

The following steps completely integrate the component into Jmix UI:

1. Create an XSD for the component (see [`theme-toggle.xsd`]({currentPath}?tab=theme-toggle.xsd)).
2. Implement the component loader (see [`ThemeToggleLoader.java`]({currentPath}?tab=ThemeToggleLoader.java)).
3. Register the component and its loader in the application (see [
   `ThemeToggleRegistration.java`]({currentPath}?tab=ThemeToggleRegistration.java)).

Once these steps are completed, the custom component can be used in view XML descriptors. See the [
`theme-toggle-usage.xml`]({currentPath}?tab=theme-toggle-usage.xml) file.

See more information about creating custom components in Vaadin
documentation: [Creating Components](https://vaadin.com/docs/latest/create-ui/creating-components),
[Using Vaadin Mixin Interfaces](https://vaadin.com/docs/latest/create-ui/creating-components/mixins), [Using
Events with Components](https://vaadin.com/docs/latest/create-ui/creating-components/events).


theme-toggle-usage.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:tt="http://io.jmix.uisamples/theme-toggle.xsd">
    <layout classNames="flex" justifyContent="CENTER" alignItems="CENTER">
        <h2 text="Theme Toggle"/>
        <tt:themeToggle id="themeToggle"
                        text="Click to switch theme"/>
    </layout>
</view>




ThemeToggleUsage.java

package io.jmix.uisamples.view.flowui.customcomponents.fromscratch;

import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.component.themetoggle.ThemeToggle;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("custom-component-from-scratch")
@ViewDescriptor("theme-toggle-usage.xml")
public class ThemeToggleUsage extends StandardView {

    @Autowired
    protected Notifications notifications;

    @Subscribe("themeToggle")
    protected void onThemeChange(ThemeToggle.ThemeToggleThemeChangedEvent event) {
        notifications.create("Theme switched: " + getThemeValue(event))
                .withPosition(Notification.Position.TOP_CENTER)
                .show();
    }

    protected String getThemeValue(ThemeToggle.ThemeToggleThemeChangedEvent event) {
        return event.getValue().isEmpty() ? "Light" : "Dark";
    }
}




ThemeToggle.java

package io.jmix.uisamples.component.themetoggle;


import com.vaadin.flow.component.*;
import com.vaadin.flow.component.dependency.JsModule;
import com.vaadin.flow.component.html.Image;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.shared.HasTooltip;
import com.vaadin.flow.dom.Element;
import com.vaadin.flow.shared.Registration;
import io.jmix.flowui.kit.component.HasTitle;
import org.springframework.lang.Nullable;

import java.util.Set;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Tag("theme-toggle")
@JsModule("./src/component/theme-switcher/theme-toggle.js")
public class ThemeToggle extends Component implements ClickNotifier<ThemeToggle>,
        Focusable<ThemeToggle>, HasTheme, HasEnabled, HasSize, HasStyle, HasText, HasTooltip, HasTitle {

    public static final String STORAGE_KEY_PROPERTY = "storageKey";
    public static final String THEME_CHANGED_EVENT = "theme-changed";
    private Component iconComponent;

    public ThemeToggle() {
        setIcon(getDefaultIcon());
    }

    public ThemeToggle(Component icon) {
        setIcon(icon);
    }

    public ThemeToggle(String text, Component icon) {
        setIcon(icon);
        setText(text);
    }

    private Icon getDefaultIcon() {
        Icon icon = VaadinIcon.ADJUST.create();
        icon.getElement().getStyle().set("rotate", "180deg");
        return icon;
    }

    /**
     * Sets the given string as the text content of this component.
     * <p>
     * This method removes any existing text-content and replaces it with the
     * given text.
     * <p>
     * This method also sets or removes this button's <code>theme=icon</code>
     * attribute based on whether this button contains only an icon after this
     * operation or not.
     *
     * @param text the text content to set, may be <code>null</code> to only
     *             remove existing text
     */
    @Override
    public void setText(@Nullable String text) {
        removeAll(getNonTextNodes());
        if (text != null && !text.isEmpty()) {
            getElement().appendChild(Element.createText(text));
        }
        updateThemeAttribute();
    }

    /**
     * Gets the component that is defined as the icon of this button.
     *
     * @return the icon of this button, or <code>null</code> if the icon is not
     * set
     */
    public Component getIcon() {
        return iconComponent;
    }

    /**
     * Sets the given component as the icon of this button.
     * <p>
     * Even though you can use almost any component as an icon, some good
     * options are {@code Icon} and {@link Image}.
     * <p>
     * This method also sets or removes this button's <code>theme=icon</code>
     * attribute based on whether this button contains only an icon after this
     * operation or not.
     *
     * @param icon component to be used as an icon, may be <code>null</code> to
     *             only remove the current icon, can't be a text-node
     */
    public void setIcon(@Nullable Component icon) {
        if (icon != null && icon.getElement().isTextNode()) {
            throw new IllegalArgumentException(
                    "Text node can't be used as an icon.");
        }
        if (iconComponent != null) {
            remove(iconComponent);
        }

        iconComponent = icon;
        if (icon != null) {
            add(icon);
            updateIconSlot();
        }

        updateThemeAttribute();
    }

    private void updateIconSlot() {
        iconComponent.getElement().setAttribute("slot", "prefix");
    }

    /**
     * Adds the given components as children of this component.
     * <p>
     * Note that using this method together with convenience methods, such as
     * {@link #setText(String)} and {@link #setIcon(Component)}, may have
     * unexpected results, e.g. in the order of child elements and the result of
     * {@link #getText()}.
     *
     * @param components the components to add
     */
    private void add(Component... components) {
        for (Component component : components) {
            assert component != null;
            getElement().appendChild(component.getElement());
        }
    }

    /**
     * Removes the given child components from this component.
     *
     * @param components The components to remove.
     * @throws IllegalArgumentException if any of the components is not a child of this component.
     */
    private void remove(Component... components) {
        for (Component component : components) {
            if (getElement().equals(component.getElement().getParent())) {
                component.getElement().removeAttribute("slot");
                getElement().removeChild(component.getElement());
            } else {
                throw new IllegalArgumentException("The given component ("
                        + component + ") is not a child of this component");
            }
        }
    }

    /**
     * Get the state for the autofocus property of the button.
     * <p>
     * This property is not synchronized automatically from the client side, so
     * the returned value may not be the same as in client side.
     *
     * @return the {@code autofocus} property from the button
     */
    public boolean isAutofocus() {
        return getElement().getProperty("autofocus", false);
    }

    /**
     * Set the button to be input focused when the page loads.
     *
     * @param autofocus the boolean value to set
     */
    public void setAutofocus(boolean autofocus) {
        getElement().setProperty("autofocus", autofocus);
    }

    public String getStorageKey() {
        return getElement().getProperty(STORAGE_KEY_PROPERTY);
    }

    public void setStorageKey(String storageKey) {
        getElement().setProperty(STORAGE_KEY_PROPERTY, storageKey);
    }

    /**
     * Removes all contents from this component except elements in
     * {@code exclusion} array. This includes child components, text content as
     * well as child elements that have been added directly to this component
     * using the {@link Element} API.
     */
    private void removeAll(Element... exclusion) {
        Set<Element> toExclude = Stream.of(exclusion)
                .collect(Collectors.toSet());
        Predicate<Element> filter = toExclude::contains;
        getElement().getChildren().filter(filter.negate())
                .forEach(child -> child.removeAttribute("slot"));
        getElement().removeAllChildren();
        getElement().appendChild(exclusion);
    }

    private Element[] getNonTextNodes() {
        return getElement().getChildren()
                .filter(element -> !element.isTextNode())
                .toArray(Element[]::new);
    }

    private void updateThemeAttribute() {
        // Add theme attribute "icon" when the button contains only an icon to
        // fully support themes like Lumo. This doesn't override explicitly set
        // theme attribute.
        long childCount = getElement().getChildren()
                .filter(el ->
                        el.isTextNode() || !"vaadin-tooltip".equals(el.getTag()))
                .count();

        if (childCount == 1 && iconComponent != null) {
            getThemeNames().add("icon");
        } else {
            getThemeNames().remove("icon");
        }
    }

    public Registration addThemeChangeListener(ComponentEventListener<ThemeToggleThemeChangedEvent> listener) {
        return addListener(ThemeToggleThemeChangedEvent.class, listener);
    }

    @DomEvent(THEME_CHANGED_EVENT)
    public static class ThemeToggleThemeChangedEvent extends ComponentEvent<ThemeToggle> {

        protected String value;

        public ThemeToggleThemeChangedEvent(ThemeToggle source, boolean fromClient,
                                            @EventData("event.detail.value") String value) {
            super(source, fromClient);
            this.value = value;
        }

        public String getValue() {
            return value;
        }
    }
}




theme-toggle.js

import {html} from "@polymer/polymer";
import {Button} from "@vaadin/button";
import {css, registerStyles} from "@vaadin/vaadin-themable-mixin";

/**
 * Use registerStyles instead of the `<style>` tag to make sure
 * that this CSS will override core styles of `vaadin-button`.
 */
registerStyles(
    'theme-toggle',
    css`
      :host {
        background: transparent;

        color: var(--lumo-text-color);
      }
    `,
    {moduleId: 'theme-toggle-styles'},
);

class ThemeToggle extends Button {

    static get is() {
        return 'theme-toggle';
    }

    static get template() {
        return html`
            <div class="vaadin-button-container">
                <span part="prefix" aria-hidden="true">
                  <slot name="prefix"></slot>
                </span>
                <span part="label">
                    <slot></slot>
                </span>
            </div>

            <slot name="tooltip"></slot>
        `;
    }

    static get properties() {
        return {
            ariaLabel: {
                type: String,
                value: 'Theme toggle',
                reflectToAttribute: true,
            },

            storageKey: {
                type: String,
                value: 'jmix.flowui.theme',
                observer: '_onStorageKeyChanged'
            }
        };
    }

    constructor() {
        super();

        this.addEventListener('click', () => this.toggleTheme());
        this.addEventListener('click', () => {
            const customEvent = new CustomEvent('theme-changed', {detail: {value: this.getCurrentTheme()}});
            this.dispatchEvent(customEvent);
        });
    }

    /** @protected */
    ready() {
        super.ready();

        this.applyStorageTheme();
    }

    applyStorageTheme() {
        let storageTheme = this.getStorageTheme();
        let currentTheme = this.getCurrentTheme();
        if (storageTheme && currentTheme !== storageTheme) {
            this.applyTheme(storageTheme);
        }
    }

    getStorageTheme() {
        return localStorage.getItem(this.storageKey);
    }

    getCurrentTheme() {
        return document.documentElement.getAttribute("theme");
    }

    toggleTheme() {
        const theme = this.getCurrentTheme();
        this.applyTheme(theme === "dark" ? "" : "dark");
    }

    applyTheme(theme) {
        document.documentElement.setAttribute("theme", theme);
        localStorage.setItem(this.storageKey, theme);
    }

    /** @protected */
    _onStorageKeyChanged(storageKey, oldStorageKey) {
        const theme = localStorage.getItem(oldStorageKey);
        localStorage.removeItem(oldStorageKey);

        if (theme) {
            localStorage.setItem(storageKey, theme);
        }
    }
}

customElements.define(ThemeToggle.is, ThemeToggle);

export {ThemeToggle};



theme-toggle.xsd

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xs:schema xmlns="http://io.jmix.uisamples/theme-toggle.xsd"
           elementFormDefault="qualified"
           targetNamespace="http://io.jmix.uisamples/theme-toggle.xsd"
           xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:layout="http://jmix.io/schema/flowui/layout">

    <xs:element name="themeToggle">
        <xs:complexType>
            <xs:complexContent>
                <xs:extension base="layout:baseComponent">
                    <xs:choice minOccurs="0">
                        <xs:element name="tooltip" type="layout:tooltipElement"/>
                    </xs:choice>

                    <xs:attribute name="autofocus" type="xs:boolean"/>
                    <xs:attribute name="themeNames" type="layout:buttonThemeNames"/>

                    <xs:attribute name="storageKey" type="xs:string"/>

                    <xs:attributeGroup ref="layout:hasText"/>
                    <xs:attributeGroup ref="layout:hasSize"/>
                    <xs:attributeGroup ref="layout:hasEnabled"/>
                    <xs:attributeGroup ref="layout:hasTitle"/>
                    <xs:attributeGroup ref="layout:hasClassNames"/>
                    <xs:attributeGroup ref="layout:hasFocusableAttributes"/>
                </xs:extension>
            </xs:complexContent>
        </xs:complexType>
    </xs:element>
</xs:schema>



ThemeToggleLoader.java

package io.jmix.uisamples.component.themetoggle;

import io.jmix.flowui.xml.layout.loader.AbstractComponentLoader;

public class ThemeToggleLoader extends AbstractComponentLoader<ThemeToggle> {

    @Override
    protected ThemeToggle createComponent() {
        return factory.create(ThemeToggle.class);
    }

    @Override
    public void loadComponent() {
        loadBoolean(element, "autofocus", resultComponent::setAutofocus);

        componentLoader().loadText(resultComponent, element);
        componentLoader().loadTitle(resultComponent, element, context);
        componentLoader().loadTooltip(resultComponent, element);
        componentLoader().loadWhiteSpace(resultComponent, element);
        componentLoader().loadEnabled(resultComponent, element);
        componentLoader().loadClassNames(resultComponent, element);
        componentLoader().loadFocusableAttributes(resultComponent, element);
        componentLoader().loadThemeNames(resultComponent, element);
        componentLoader().loadSizeAttributes(resultComponent, element);
    }
}




ThemeToggleRegistration.java

package io.jmix.uisamples.view.flowui.customcomponents.fromscratch;

import io.jmix.flowui.sys.registration.ComponentRegistration;
import io.jmix.flowui.sys.registration.ComponentRegistrationBuilder;
import io.jmix.uisamples.component.themetoggle.ThemeToggle;
import io.jmix.uisamples.component.themetoggle.ThemeToggleLoader;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ThemeToggleRegistration {

    @Bean
    public ComponentRegistration themeToggle() {
        return ComponentRegistrationBuilder.create(ThemeToggle.class)
                .withComponentLoader("themeToggle", ThemeToggleLoader.class)
                .build();
    }
}


