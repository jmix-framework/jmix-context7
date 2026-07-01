<Path>Custom components > Integrating JavaScript library</Path>

You can create custom UI components based on third-party JavaScript libraries. This example demonstrates integration of the jQuery UI Slider widget and its usage in a Jmix view. The Slider.js file located in the frontend/src/component/slider folder contains a web component wrapping the jQuery UI Slider widget. Its ready() method is used to initialize the widget. The server-side part of the custom component is defined in Slider.java. It contains a number of annotations for integration with the client-side part: @Tag - specifies the name of the custom HTML element of the web component. @NpmPackage imports an NPM module. @JsModule - imports a JavaScript module. @CssImport - imports styles. After creating the client-side and server-side parts of the component, it can be used in views by creating an instance of its Java class and adding it to a parent component. The following steps completely integrate the component into Jmix UI: Create an XSD for the component (see slider.xsd). Implement the component loader (see SliderLoader.java). Register the component and its loader in the application (see SliderComponentRegistration.java). Once these steps are completed, the custom component can be used in view XML descriptors. See the slider-usage.xml file. See more information about creating custom components in Vaadin documentation: Importing JavaScript & CSS, Integrating Web Components, Element API.

slider-usage.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:sl="http://io.jmix.uisamples/slider.xsd">
    <layout justifyContent="CENTER" alignItems="CENTER">
        <h2 text="Slider"/>
        <sl:slider id="slider"
                   width="15em"
                   minHeight="0.8em"
                   max="100" min="10" value="50"/>
    </layout>
</view>




SliderUsage.java

package io.jmix.uisamples.view.flowui.customcomponents.jslibrary;

import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.component.slider.Slider;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("custom-component-js-library")
@ViewDescriptor("slider-usage.xml")
public class SliderUsage extends StandardView {

    @Autowired
    protected Notifications notifications;

    @Subscribe("slider")
    protected void onSliderChange(Slider.SlideChangedEvent event) {
        notifications.create("New value is : " + event.getValue())
                .withPosition(Notification.Position.TOP_CENTER)
                .show();
    }
}




Slider.java

package io.jmix.uisamples.component.slider;

import com.vaadin.flow.component.*;
import com.vaadin.flow.component.dependency.CssImport;
import com.vaadin.flow.component.dependency.JsModule;
import com.vaadin.flow.component.dependency.NpmPackage;
import com.vaadin.flow.shared.Registration;

@Tag("demo-slider")
@NpmPackage(value = "jquery", version = "1.9.1")
@NpmPackage(value = "jquery-ui", version = "1.13.2")
@CssImport("jquery-ui/dist/themes/base/jquery-ui.css")
@JsModule("./src/component/slider/slider.js")
public class Slider extends Component implements HasSize {

    public static final String VALUE_PROPERTY = "value";
    public static final String MIN_PROPERTY = "min";
    public static final String MAX_PROPERTY = "max";
    public static final String SLIDE_CHANGED_EVENT = "custom-slide-changed";

    public Slider() {
    }

    public int getMin() {
        return getElement().getProperty(MIN_PROPERTY, 0);
    }

    public void setMin(int min) {
        getElement().setProperty(MIN_PROPERTY, min);
    }

    public int getMax() {
        return getElement().getProperty(MAX_PROPERTY, 100);
    }

    public void setMax(int max) {
        getElement().setProperty(MAX_PROPERTY, max);
    }

    @Synchronize(property = VALUE_PROPERTY, value = SLIDE_CHANGED_EVENT)
    public int getValue() {
        return getElement().getProperty(VALUE_PROPERTY, 0);
    }

    public void setValue(int value) {
        getElement().setProperty(VALUE_PROPERTY, value);
    }

    public Registration addValueChangeListener(ComponentEventListener<SlideChangedEvent> listener) {
        return addListener(SlideChangedEvent.class, listener);
    }

    @DomEvent(SLIDE_CHANGED_EVENT)
    public static class SlideChangedEvent extends ComponentEvent<Slider> {

        protected int value;

        public SlideChangedEvent(Slider source, boolean fromClient,
                                 @EventData("event.detail.value") int value) {
            super(source, fromClient);
            this.value = value;
        }

        public int getValue() {
            return value;
        }
    }
}




slider.js

import 'jquery/jquery.js'
import 'jquery-ui/dist/jquery-ui.js'
import {LitElement} from 'lit';
import {ElementMixin} from '@vaadin/component-base/src/element-mixin.js';
import {defineCustomElement} from '@vaadin/component-base/src/define.js';
import {PolylitMixin} from '@vaadin/component-base/src/polylit-mixin.js';

export class Slider extends ElementMixin(PolylitMixin(LitElement)) {

    static get is() {
        return 'demo-slider';
    }

    static get properties() {
        return {
            min: {
                type: Number,
                value: 0,
                observer: '_onMinChange'
            },

            max: {
                type: Number,
                value: 100,
                observer: '_onMaxChange'
            },

            value: {
                type: Number,
                notify: true,
                observer: '_onValueChange'
            },

            /** @private */
            _slider: {
                type: Object
            }
        }
    }

    // to disable shadow dom
    createRenderRoot() {
        return this;
    }

    ready() {
        super.ready();

        let $jQuery = jQuery.noConflict();
        this._slider = $jQuery(this);
        this._slider.slider({
            min: this.min,
            max: this.max,

            change: function (event, ui) {
                if (this.value === ui.value) {
                    return;
                }
                this.value = ui.value;
                const slideChangeEvent = new CustomEvent(
                    'custom-slide-changed',
                    {detail: {value: ui.value}}
                );
                this.dispatchEvent(slideChangeEvent);
            }
        });
    }

    /**
     * @protected
     */
    _onValueChange(value) {
        if (this._slider === undefined) {
            return;
        }

        this._slider.slider("value", value);
    }

    /**
     * @protected
     */
    _onMinChange(value) {
        if (this._slider === undefined) {
            return;
        }

        this._slider.slider("option", "min", value);
    }

    /**
     * @protected
     */
    _onMaxChange(value) {
        if (this._slider === undefined) {
            return;
        }

        this._slider.slider("option", "max", value);
    }
}

defineCustomElement(Slider);




slider.xsd

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xs:schema xmlns="http://io.jmix.uisamples/slider.xsd"
           elementFormDefault="qualified"
           targetNamespace="http://io.jmix.uisamples/slider.xsd"
           xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:layout="http://jmix.io/schema/flowui/layout">

    <xs:element name="slider">
        <xs:complexType>
            <xs:complexContent>
                <xs:extension base="layout:baseComponent">
                    <xs:attribute name="min" type="xs:integer"/>
                    <xs:attribute name="max" type="xs:integer"/>
                    <xs:attribute name="value" type="xs:integer"/>

                    <xs:attributeGroup ref="layout:hasSize"/>
                </xs:extension>
            </xs:complexContent>
        </xs:complexType>
    </xs:element>

</xs:schema>



SliderLoader.java

package io.jmix.uisamples.component.slider;

import io.jmix.flowui.xml.layout.loader.AbstractComponentLoader;

public class SliderLoader extends AbstractComponentLoader<Slider> {

    @Override
    protected Slider createComponent() {
        return factory.create(Slider.class);
    }

    @Override
    public void loadComponent() {
        loadInteger(element, "min", resultComponent::setMin);
        loadInteger(element, "max", resultComponent::setMax);
        loadInteger(element, "value", resultComponent::setValue);

        componentLoader().loadSizeAttributes(resultComponent, element);
    }
}




SliderComponentRegistration.java

package io.jmix.uisamples.view.flowui.customcomponents.jslibrary;

import io.jmix.flowui.sys.registration.ComponentRegistration;
import io.jmix.flowui.sys.registration.ComponentRegistrationBuilder;
import io.jmix.uisamples.component.slider.Slider;
import io.jmix.uisamples.component.slider.SliderLoader;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SliderComponentRegistration {

    @Bean
    public ComponentRegistration slider() {
        return ComponentRegistrationBuilder.create(Slider.class)
                .withComponentLoader("slider", SliderLoader.class)
                .build();
    }
}

