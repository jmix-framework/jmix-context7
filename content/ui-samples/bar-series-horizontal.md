<Path>Add-ons > Charts > Series > Bar series > Horizontal Bar series</Path>

To lay the bars out horizontally, swap the axes: the category axis becomes a `yAxis` with `type="CATEGORY"`, and the value axis becomes an `xAxis` with `type="VALUE"`.

`showBackground` draws a track behind each bar, and `backgroundStyle` sets its look. `borderRadius` in `itemStyle` rounds the corners of the bars. A `label` with the `RIGHT` position shows the value next to each bar.

The category axis lists the items from the bottom up. The query sorts the countries by `litres`, so the longest bar is at the top.


bar-series-horizontal.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="countryLitresDc"
                    class="io.jmix.uisamples.entity.CountryLitres"
                    fetchPlan="_local">
            <loader id="countryLitresDl" readOnly="true">
                <query>
                    <![CDATA[select e from CountryLitres e order by e.litres]]>
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
            <charts:tooltip trigger="AXIS">
                <charts:axisPointer type="SHADOW"/>
            </charts:tooltip>

            <charts:xAxes>
                <charts:xAxis type="VALUE"/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis type="CATEGORY"/>
            </charts:yAxes>

            <charts:dataSet>
                <charts:source dataContainer="countryLitresDc"
                               categoryField="country" valueFields="litres"/>
            </charts:dataSet>

            <charts:series>
                <charts:bar name="Liters" showBackground="true">
                    <charts:label show="true" position="RIGHT"/>
                </charts:bar>
            </charts:series>
        </charts:chart>
    </layout>
</view>




BarSeriesHorizontalSample.java

package io.jmix.uisamples.view.flowui.charts.series.bar.horizontal;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("bar-series-horizontal")
@ViewDescriptor("bar-series-horizontal.xml")
public class BarSeriesHorizontalSample extends StandardView {
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


