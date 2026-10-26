<Path>Custom components > Integrating Vaadin add-ons > Integrating SO Chart add-on</Path>

You can use any third-party Vaadin add-ons located in the Vaadin Directory or elsewhere. This example demonstrates the integration of the SO Charts add-on. To include the Vaadin add-on in your application, add the Vaadin Add-ons maven repository and the add-on dependency to the project's build.gradle: repositories {
    maven {
        url 'https://maven.vaadin.com/vaadin-addons'
    }
    // ...
}

dependencies {
    implementation 'org.vaadin.addons.so:so-charts:6.0.1'
    // ...
} After that, you can use the add-on components programmatically, see for example ChartsAddonSample.java. To be able to use the add-on components in views XML declaratively, a few more steps are needed: Create an XSD for the components (see chart.xsd) Implement the component loaders (see ChartLoader.java). Register the components and its loaders in the application (see ChartComponentRegistration.java). Note: This example provides only partial support for the add-on components (not all components and properties are described for usage in XML).

charts-addon.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:chart="http://io.jmix.uisamples/chart.xsd">
    <layout padding="false">
        <tabSheet id="tabSheet" width="100%">
            <tab id="barChartTab" label="Declaratively added bar chart">
                <chart:sochart width="99%" minHeight="30em"
                             labels="Backlog, Next, In-progress, Review, QA, Done"
                             data="18, 8, 5, 6, 29, 53">
                    <chart:barChart name="Bars"/>
                    <chart:toolbox>
                        <chart:buttons>
                            <chart:button type="zoom"/>
                            <chart:button type="download"/>
                        </chart:buttons>
                    </chart:toolbox>
                    <chart:title text="Issues by status"
                                 subText="The current status is presented in bars"/>
                </chart:sochart>
            </tab>
            <tab id="roseChart" label="Declaratively added rose chart">
                <chart:sochart width="99%" minHeight="30em"
                             labels="Backlog, Next, In-progress, Review, QA, Done"
                             data="18, 8, 5, 6, 29, 53">
                    <chart:nightingaleRoseChart name="Issue"/>
                    <chart:title text="Issues by status"
                                 subText="The current status is presented in rose chart"/>
                </chart:sochart>
            </tab>
        </tabSheet>
    </layout>
</view>




ChartsAddonSample.java

package io.jmix.uisamples.view.flowui.customcomponents.vaadinaddons.socharts;

import com.storedobject.chart.*;
import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.tabs.Tab;
import io.jmix.flowui.component.tabsheet.JmixTabSheet;
import io.jmix.flowui.view.*;

import java.util.Random;

@ViewController("charts-addon")
@ViewDescriptor("charts-addon.xml")
public class ChartsAddonSample extends StandardView {

    @ViewComponent
    protected JmixTabSheet tabSheet;

    @Subscribe
    protected void onInit(InitEvent event) {
        Component lineChart = createLineChart();

        Tab tab = new Tab("Programmatically added line chart");
        tab.setId("lineChart");

        tabSheet.add(tab, lineChart);
    }

    protected Component createLineChart() {
        SOChart rootChart = new SOChart();
        rootChart.setWidthFull();
        rootChart.setMinHeight("30em");

        Random random = new Random();
        Data xValues = new Data();
        Data yValues = new Data();

        for (int x = 0; x < 40; x++) {
            xValues.add(x);
            yValues.add(random.nextDouble());
        }

        xValues.setName("Time per feature per day");
        yValues.setName("Percentage");

        LineChart lineChart = new LineChart(xValues, yValues);
        lineChart.setName("Percentage of time spent on a feature");

        XAxis xAxis = new XAxis(DataType.NUMBER);
        YAxis yAxis = new YAxis(DataType.NUMBER);
        RectangularCoordinate rc = new RectangularCoordinate(xAxis, yAxis);
        lineChart.plotOn(rc);

        rootChart.add(lineChart, new Title("Feature statistic"));

        return rootChart;
    }
}




chart.xsd

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xs:schema xmlns="http://io.jmix.uisamples/chart.xsd"
           elementFormDefault="qualified"
           targetNamespace="http://io.jmix.uisamples/chart.xsd"
           xmlns:xs="http://www.w3.org/2001/XMLSchema"
           xmlns:layout="http://jmix.io/schema/flowui/layout">

    <xs:element name="sochart">
        <xs:complexType>
            <xs:complexContent>
                <xs:extension base="layout:baseComponent">
                    <xs:sequence>
                        <xs:group ref="chartComponents"/>
                    </xs:sequence>

                    <xs:attribute name="labels" type="xs:string"/>
                    <xs:attribute name="data" type="xs:string"/>

                    <xs:attributeGroup ref="layout:hasSize"/>
                </xs:extension>
            </xs:complexContent>
        </xs:complexType>
    </xs:element>

    <xs:group name="chartComponents">
        <xs:sequence>
            <xs:choice maxOccurs="unbounded">
                <xs:element name="nightingaleRoseChart" type="baseChart"/>
                <xs:element name="barChart" type="baseChart"/>
                <xs:element name="toolbox" type="toolbox"/>
                <xs:element name="title" type="title"/>
            </xs:choice>
        </xs:sequence>
    </xs:group>

    <xs:complexType name="baseChart">
        <xs:attribute name="name" type="xs:string"/>
    </xs:complexType>

    <xs:complexType name="toolbox">
        <xs:sequence maxOccurs="unbounded">
            <xs:element name="buttons" type="toolboxButtons"/>
        </xs:sequence>
    </xs:complexType>

    <xs:complexType name="toolboxButtons">
        <xs:sequence>
            <xs:element name="button">
                <xs:complexType>
                    <xs:attribute name="type" type="toolboxButtonType"/>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>

    <xs:simpleType name="toolboxButtonType">
        <xs:restriction>
            <xs:enumeration value="download"/>
            <xs:enumeration value="restore"/>
            <xs:enumeration value="zoom"/>
            <xs:enumeration value="data-view"/>
        </xs:restriction>
    </xs:simpleType>

    <xs:complexType name="title">
        <xs:attribute name="text" type="xs:string"/>
        <xs:attribute name="subText" type="xs:string"/>
    </xs:complexType>
</xs:schema>



ChartLoader.java

package io.jmix.uisamples.component.chart;

import com.google.common.base.Strings;
import com.storedobject.chart.*;
import io.jmix.flowui.exception.GuiDevelopmentException;
import io.jmix.flowui.xml.layout.loader.AbstractComponentLoader;
import org.dom4j.Element;

import java.util.Arrays;

public class ChartLoader extends AbstractComponentLoader<SOChart> {

    protected CategoryData predefinedLabels;
    protected Data predefinedData;

    @Override
    protected SOChart createComponent() {
        return factory.create(SOChart.class);
    }

    @Override
    public void loadComponent() {
        componentLoader().loadSizeAttributes(resultComponent, element);

        loadLabels(element);
        loadData(element);
        loadSubComponents(resultComponent, element);
    }

    protected void loadLabels(Element element) {
        String[] labels = loadString(element, "labels")
                .map(this::split)
                .orElse(null);

        predefinedLabels = new CategoryData(labels);
    }

    protected void loadData(Element element) {
        Number[] data = loadString(element, "data")
                .map(this::split)
                .map(this::mapToNumbers)
                .orElse(null);

        predefinedData = new Data(data);

        if (predefinedData.asList().size() != predefinedLabels.asList().size()) {
            throw new GuiDevelopmentException("Chart's data and labels must be the same size", context);
        }
    }

    protected void loadSubComponents(SOChart resultComponent, Element element) {
        for (Element nestedElement : element.elements()) {
            Component subComponent = switch (nestedElement.getName()) {
                case "nightingaleRoseChart" -> loadNightingaleRoseChart(nestedElement);
                case "barChart" -> loadBarChart(nestedElement);
                case "toolbox" -> loadToolbox(nestedElement);
                case "title" -> loadTitle(nestedElement);
                default -> throw new GuiDevelopmentException("Unknown nested tag", context);
            };

            resultComponent.add(subComponent);
        }
    }

    protected NightingaleRoseChart loadNightingaleRoseChart(Element element) {
        NightingaleRoseChart nightingaleRoseChart = new NightingaleRoseChart(predefinedLabels, predefinedData);
        loadString(element, "name", nightingaleRoseChart::setName);
        return nightingaleRoseChart;
    }

    protected BarChart loadBarChart(Element element) {
        BarChart barChart = new BarChart(predefinedLabels, predefinedData);

        RectangularCoordinate coordinate =
                new RectangularCoordinate(new XAxis(DataType.CATEGORY), new YAxis(DataType.NUMBER));
        barChart.plotOn(coordinate);

        loadString(element, "name", barChart::setName);

        return barChart;
    }

    protected Toolbox loadToolbox(Element element) {
        Element buttons = element.element("buttons");

        if (buttons == null) {
            throw new GuiDevelopmentException("Buttons are required for Toolbox", context);
        }

        Toolbox toolbox = new Toolbox();

        for (Element button : buttons.elements()) {
            loadString(button, "type")
                    .map(this::toolboxButtonMapper)
                    .ifPresent(toolbox::addButton);
        }

        return toolbox;
    }

    protected Title loadTitle(Element element) {
        String text = loadString(element, "text")
                .orElseThrow(() -> new GuiDevelopmentException("Required attribute 'text' is not found", context));

        Title title = new Title(text);
        loadString(element, "subText", title::setSubtext);

        return title;
    }

    protected ToolboxButton toolboxButtonMapper(String type) {
        return switch (type) {
            case "download" -> new Toolbox.Download();
            case "restore" -> new Toolbox.Restore();
            case "zoom" -> new Toolbox.Zoom();
            case "data-view" -> new Toolbox.DataView();
            default -> throw new GuiDevelopmentException("Unknown toolbox button type", context);
        };
    }

    protected String[] split(String names) {
        return Arrays.stream(names.split("[\\s,]+"))
                .filter(split -> !Strings.isNullOrEmpty(split))
                .toArray(String[]::new);
    }

    protected Number[] mapToNumbers(String[] strings) {
        return Arrays.stream(strings)
                .map(Double::valueOf)
                .toArray(Number[]::new);
    }
}




ChartComponentRegistration.java

package io.jmix.uisamples.view.flowui.customcomponents.vaadinaddons.socharts;

import com.storedobject.chart.SOChart;
import io.jmix.flowui.sys.registration.ComponentRegistration;
import io.jmix.flowui.sys.registration.ComponentRegistrationBuilder;
import io.jmix.uisamples.component.chart.ChartLoader;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ChartComponentRegistration {

    @Bean
    public ComponentRegistration soChart() {
        return ComponentRegistrationBuilder.create(SOChart.class)
                .withComponentLoader("sochart", ChartLoader.class)
                .build();
    }
}


