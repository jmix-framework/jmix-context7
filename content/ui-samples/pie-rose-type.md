<Path>Add-ons > Charts > Series > Pie series > Nightingale Chart</Path>

The Nightingale's Rose chart is a circular graph that combines elements of a radar chart and a column graph. roseType property configures whether to show as Nightingale chart, which distinguishes data through radius. There are 2 optional modes: RADIUS - use central angle to show the percentage of data, radius to show data size. AREA - all the sectors will share the same central angle, the data size is shown only through radius.

pie-rose-type.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="countryLitresDc"
                    class="io.jmix.uisamples.entity.CountryLitres"
                    fetchPlan="_local">
            <loader id="countryLitresDl" readOnly="true">
                <query>
                    <![CDATA[select e from CountryLitres e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Liters" subtext="By countries" left="0" top="0"/>
            <charts:legend top="0"/>
            <charts:tooltip trigger="ITEM"/>

            <charts:dataSet>
                <charts:source dataContainer="countryLitresDc"
                               categoryField="country" valueFields="litres"/>
            </charts:dataSet>

            <charts:series>
                <charts:pie name="Radius" center="25% 50%" roseType="RADIUS"
                            radius="20 175">
                    <charts:label formatter="{b}: {d}%"/>
                </charts:pie>
                <charts:pie name="Area" center="75% 50%" roseType="AREA"
                            radius="20 175">
                    <charts:label formatter="{b}: {d}%"/>
                </charts:pie>
            </charts:series>
        </charts:chart>
    </layout>
</view>




PieRoseTypeSample.java

package io.jmix.uisamples.view.flowui.charts.series.pie.rosetype;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("pie-rose-type")
@ViewDescriptor("pie-rose-type.xml")
public class PieRoseTypeSample extends StandardView {
}




CountryLitres.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@JmixEntity
@Table(name = "COUNTRY_LITRES")
@Entity
public class CountryLitres {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @NotNull
    @Column(name = "COUNTRY", nullable = false)
    private String country;

    @NotNull
    @Column(name = "LITRES", nullable = false)
    private Double litres;

    public Double getLitres() {
        return litres;
    }

    public void setLitres(Double litres) {
        this.litres = litres;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}


