<Path>Add-ons > Charts > Series > Pie series > Simple Pie series</Path>

PieSeries (or a circle chart) is a circular statistical graphic, which is divided into slices to illustrate numerical proportion. Each arc length represents the proportion of data quantity.

pie-series-simple.xml

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
            <charts:title text="Liters" subtext="By countries"/>
            <charts:legend top="0"/>
            <charts:tooltip trigger="ITEM"/>

            <charts:dataSet>
                <charts:source dataContainer="countryLitresDc"
                               categoryField="country" valueFields="litres"/>
            </charts:dataSet>

            <charts:series>
                <charts:pie name="Liters">
                    <charts:label formatter="{b}: {d}%"/>
                </charts:pie>
            </charts:series>
        </charts:chart>
    </layout>
</view>




PieSeriesSimpleSample.java

package io.jmix.uisamples.view.flowui.charts.series.pie.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("pie-series-simple")
@ViewDescriptor("pie-series-simple.xml")
public class PieSeriesSimpleSample extends StandardView {
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


