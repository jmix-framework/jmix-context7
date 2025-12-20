<Path>Add-ons > Charts > Series > Radar series > Simple Radar series</Path>

RadarSeries is mainly used to show multi-variable data. Please note that to determine the RadarSeries, it is necessary to determine the radar coordinate component, with the corresponding indicators.

radar-series-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:radar>
                <charts:indicators>
                    <charts:indicator name="Russia" max="300"/>
                    <charts:indicator name="Ireland" max="300"/>
                    <charts:indicator name="Germany" max="300"/>
                    <charts:indicator name="Australia" max="300"/>
                    <charts:indicator name="Austria" max="300"/>
                    <charts:indicator name="UK" max="300"/>
                    <charts:indicator name="Belgium" max="300"/>
                </charts:indicators>
            </charts:radar>

            <charts:series>
                <charts:radar/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




RadarSeriesSimpleSample.java

package io.jmix.uisamples.view.flowui.charts.series.radar.simple;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.util.Map;

@ViewController("radar-series-simple")
@ViewDescriptor("radar-series-simple.xml")
public class RadarSeriesSimpleSample extends StandardView {

    @ViewComponent
    protected Chart chart;

    @Subscribe
    protected void onInit(InitEvent event) {
        ListChartItems<MapDataItem> items = new ListChartItems<>(
                new MapDataItem(
                        Map.of(
                                "Russia", 256.9,
                                "Ireland", 131.1,
                                "Germany", 115.8,
                                "Australia", 109.9,
                                "Austria", 108.3,
                                "UK", 65.0,
                                "Belgium", 40.0
                        )
                )
        );

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(items)
                                        .withValueFields(
                                                "Russia",
                                                "Ireland",
                                                "Germany",
                                                "Australia",
                                                "Austria",
                                                "UK",
                                                "Belgium"
                                        )
                        )
        );
    }
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


