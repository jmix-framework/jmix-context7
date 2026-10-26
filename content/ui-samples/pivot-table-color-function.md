<Path>Add-ons > PivotTable > PivotTable color function</Path>

PivotTable supports the custom color function for Heatmap renderer.

pivot-table-color-function.xml

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
                           showRowTotals="false"
                           renderer="HEATMAP">
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
            </pvttbl:rows>
            <pvttbl:aggregation mode="AVERAGE">
                <pvttbl:property name="temperature"/>
            </pvttbl:aggregation>
            <pvttbl:rendererOptions>
                <pvttbl:heatmap>
                    <pvttbl:colorScaleGeneratorFunction><![CDATA[
                        function(values) {
                            var max, min;
                            min = Math.min.apply(Math, values);
                            max = Math.max.apply(Math, values);

                            return function(x) {
                                let fromR, fromG, fromB;
                                let toR, toG, toB;
                                if (x < 0) {
                                    min = -35;
                                    max = 0;
                                    fromR = 0, fromG = 0, fromB = 255;
                                    toR = 255, toG = 255, toB = 255;
                                } else {
                                    min = 0;
                                    max = 35;
                                    fromR = 255, fromG = 255, fromB = 255;
                                    toR = 255, toG = 0, toB = 0;
                                }

                                let interpolationRatio = (x - min) / (max - min);
                                let r = fromR - Math.round((fromR - toR) * interpolationRatio);
                                let g = fromG - Math.round((fromG - toG) * interpolationRatio);
                                let b = fromB - Math.round((fromB - toB) * interpolationRatio);
                                return "rgb(" + r + ", " + g + ", " + b +")";
                            }
                        }]]>
                    </pvttbl:colorScaleGeneratorFunction>
                </pvttbl:heatmap>
            </pvttbl:rendererOptions>
        </pvttbl:pivotTable>
    </layout>
</view>



PivotTableColorFunction.java

package io.jmix.uisamples.view.flowui.pivottable.colorfunction;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("pivot-table-color-function")
@ViewDescriptor("pivot-table-color-function.xml")
public class PivotTableColorFunction extends StandardView {
}




TemperatureData.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.jspecify.annotations.Nullable;

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
    private Double temperature;

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

    public Double getTemperature() {
        return temperature;
    }

    public void setTemperature(Double temperature) {
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


