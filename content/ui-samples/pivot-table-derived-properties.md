<Path>Add-ons > PivotTable > PivotTable derived properties</Path>

PivotTable supports the addition of new properties derived from existing ones. In this example we have temperature measurements in Celsius. But we want to see data in Fahrenheit. To do this we need to complete the next steps: Define the name of the derived property. Write a javascript function. Important note: in the function we need to use localized names of the properties. Initialize the DerivedProperties object.

pivot-table-derived-properties.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:pvttbl="http://jmix.io/schema/pvttbl/ui">
    <data>
        <collection id="temperatureDataDc"
                    class="io.jmix.uisamples.entity.TemperatureData">
            <fetchPlan extends="_local"/>
            <loader id="tipsLoader">
                <query>
                    <![CDATA[select e from TemperatureData e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <pvttbl:pivotTable id="pivotTable"
                           dataContainer="temperatureDataDc"
                           showColumnTotals="false"
                           showRowTotals="false">
            <pvttbl:properties>
                <pvttbl:property name="temperature"/>
                <pvttbl:property name="city"/>
                <pvttbl:property name="month"/>
            </pvttbl:properties>
            <pvttbl:columns>
                <pvttbl:column value="city"/>
            </pvttbl:columns>
            <pvttbl:rows>
                <pvttbl:row value="month"/>
                <pvttbl:row value="msg://temperature.fahrenheit"/>
            </pvttbl:rows>
            <pvttbl:aggregation mode="AVERAGE">
                <pvttbl:property name="temperature"/>
            </pvttbl:aggregation>
        </pvttbl:pivotTable>
    </layout>
</view>



PivotTableDerivedProperties.java

package io.jmix.uisamples.view.flowui.pivottable.derivedproperties;

import io.jmix.core.MessageTools;
import io.jmix.core.Metadata;
import io.jmix.core.metamodel.model.MetaClass;
import io.jmix.flowui.view.*;
import io.jmix.pivottableflowui.component.PivotTable;
import io.jmix.pivottableflowui.kit.component.model.DerivedProperties;
import io.jmix.pivottableflowui.kit.component.model.JsFunction;
import io.jmix.uisamples.entity.TemperatureData;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Map;

@ViewController("pivot-table-derived-properties")
@ViewDescriptor("pivot-table-derived-properties.xml")
public class PivotTableDerivedProperties extends StandardView {

    @ViewComponent
    private PivotTable<TemperatureData> pivotTable;
    @ViewComponent
    private MessageBundle messageBundle;

    @Autowired
    private Metadata metadata;
    @Autowired
    private MessageTools messageTools;

    @Subscribe
    public void onInit(final InitEvent event) {
        MetaClass metaClass = metadata.getClass(TemperatureData.class);
        String temperatureCaption = messageTools.getPropertyCaption(metaClass, "temperature");

        String formattedFunction = """
                function(record) {
                    return pivotTable.$jQuery.pivotUtilities.numberFormat()(record.%s * 1.8 + 32);
                }
                """.formatted(temperatureCaption);

        DerivedProperties derivedProperties = new DerivedProperties();
        Map<String, JsFunction> propertiesMap = Map.of(
                messageBundle.getMessage("temperature.fahrenheit"),
                new JsFunction(formattedFunction)
        );

        derivedProperties.setProperties(propertiesMap);
        pivotTable.setDerivedProperties(derivedProperties);
    }
}




TemperatureData.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.springframework.lang.Nullable;

import java.util.UUID;

@JmixEntity
@Table(name = "TEMPERATURE_DATA")
@Entity
public class TemperatureData {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "TEMPERATURE", nullable = false)
    private Integer temperature;

    @Column(name = "CITY", nullable = false)
    private String city;

    @Column(name = "MONTH_")
    private String month;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public Integer getTemperature() {
        return temperature;
    }

    public void setTemperature(Integer temperature) {
        this.temperature = temperature;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    @Nullable
    public Month getMonth() {
        return month == null? null :Month.fromId(month);
    }

    public void setMonth(@Nullable Month month) {
        this.month = month == null ? null : month.getId();
    }
}


