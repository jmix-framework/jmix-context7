<Path>Add-ons > Charts > Series > Bar series > Polar Bar series</Path>

A `bar` series with `coordinateSystem="POLAR"` is drawn in polar coordinates instead of rectangular ones. The `polar` element sets the size of the polar area, and the `radiusAxis` and `angleAxis` elements replace the X and Y axes.

Here the countries are on the radius axis, so each bar is an arc. `encode` maps the data fields to the axes: `radius` takes the category, `angle` takes the value.

The `maxFunction` of the angle axis sets its maximum to 4/3 of the largest value, so the longest arc takes three quarters of the circle.


bar-series-polar.xml

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
            <charts:tooltip trigger="ITEM"/>

            <charts:polar radius="15% 80%"/>
            <charts:radiusAxis type="CATEGORY"/>
            <charts:angleAxis type="VALUE" maxFunction="function (value) { return value.max * 4 / 3; }"/>

            <charts:dataSet>
                <charts:source dataContainer="countryLitresDc"
                               categoryField="country" valueFields="litres"/>
            </charts:dataSet>

            <charts:series>
                <charts:bar name="Liters" coordinateSystem="POLAR">
                    <charts:encode radius="country" angle="litres"/>
                </charts:bar>
            </charts:series>

            <charts:nativeJson>
                <![CDATA[
                {
                    "series": [
                        {
                            "itemStyle": {
                                "borderRadius": [0, "50%", 0, "50%"]
                            }
                        }
                    ]
                }
                ]]>
            </charts:nativeJson>
        </charts:chart>
    </layout>
</view>




BarSeriesPolarSample.java

package io.jmix.uisamples.view.flowui.charts.series.bar.polar;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("bar-series-polar")
@ViewDescriptor("bar-series-polar.xml")
public class BarSeriesPolarSample extends StandardView {
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


