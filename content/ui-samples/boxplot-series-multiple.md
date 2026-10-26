<Path>Add-ons > Charts > Series > Boxplot series > Multiple Boxplot series</Path>

Several `boxplot` series on one category axis are placed side by side, so you can compare the distributions within each category. Here each series is a season, and each category is a city.

All series read the same data set: each row holds five values for every season, and each series picks its own five fields with `encode`, for the value axis and for the tooltip.

The chart doesn't calculate the statistics, so the controller does it. It loads the monthly temperatures of the `TemperatureData` entity, groups them by city and season, and calculates the minimum, the quartiles, the median and the maximum of each group.


boxplot-series-multiple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Temperature" subtext="°C, by seasons" left="0" top="0"/>
            <charts:legend top="0"/>
            <charts:tooltip trigger="ITEM"/>

            <charts:xAxes>
                <charts:xAxis type="CATEGORY"/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis/>
            </charts:yAxes>

            <charts:series>
                <charts:boxplot name="Winter">
                    <charts:encode x="city" y="winterMin, winterQ1, winterMedian, winterQ3, winterMax"
                                   tooltip="winterMin, winterQ1, winterMedian, winterQ3, winterMax"/>
                </charts:boxplot>
                <charts:boxplot name="Spring">
                    <charts:encode x="city" y="springMin, springQ1, springMedian, springQ3, springMax"
                                   tooltip="springMin, springQ1, springMedian, springQ3, springMax"/>
                </charts:boxplot>
                <charts:boxplot name="Summer">
                    <charts:encode x="city" y="summerMin, summerQ1, summerMedian, summerQ3, summerMax"
                                   tooltip="summerMin, summerQ1, summerMedian, summerQ3, summerMax"/>
                </charts:boxplot>
                <charts:boxplot name="Autumn">
                    <charts:encode x="city" y="autumnMin, autumnQ1, autumnMedian, autumnQ3, autumnMax"
                                   tooltip="autumnMin, autumnQ1, autumnMedian, autumnQ3, autumnMax"/>
                </charts:boxplot>
            </charts:series>
        </charts:chart>
    </layout>
</view>




BoxplotSeriesMultipleSample.java

package io.jmix.uisamples.view.flowui.charts.series.boxplot.multiple;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.core.DataManager;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Month;
import io.jmix.uisamples.entity.TemperatureData;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

@ViewController("boxplot-series-multiple")
@ViewDescriptor("boxplot-series-multiple.xml")
public class BoxplotSeriesMultipleSample extends StandardView {

    private static final List<String> SEASONS = List.of("winter", "spring", "summer", "autumn");
    private static final List<String> STATISTICS = List.of("Min", "Q1", "Median", "Q3", "Max");
    private static final double[] QUANTILES = {0, 0.25, 0.5, 0.75, 1};

    @Autowired
    private DataManager dataManager;

    @ViewComponent
    private Chart chart;

    @Subscribe
    public void onInit(InitEvent event) {
        Map<String, Map<String, List<Double>>> temperatures = dataManager.load(TemperatureData.class)
                .all()
                .list()
                .stream()
                .collect(Collectors.groupingBy(TemperatureData::getCity, TreeMap::new,
                        Collectors.groupingBy(data -> getSeason(data.getMonth()),
                                Collectors.mapping(TemperatureData::getTemperature, Collectors.toList()))));

        ListChartItems<MapDataItem> items = new ListChartItems<>();
        temperatures.forEach((city, seasonTemperatures) -> {
            MapDataItem item = new MapDataItem().add("city", city);
            seasonTemperatures.forEach((season, values) -> addStatistics(item, season, values));
            items.addItem(item);
        });

        String[] valueFields = SEASONS.stream()
                .flatMap(season -> STATISTICS.stream().map(statistic -> season + statistic))
                .toArray(String[]::new);

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(items)
                                        .withCategoryField("city")
                                        .withValueFields(valueFields)
                        )
        );
    }

    private String getSeason(Month month) {
        return switch (month) {
            case DECEMBER, JANUARY, FEBRUARY -> "winter";
            case MARCH, APRIL, MAY -> "spring";
            case JUNE, JULY, AUGUST -> "summer";
            case SEPTEMBER, OCTOBER, NOVEMBER -> "autumn";
        };
    }

    private void addStatistics(MapDataItem item, String season, List<Double> values) {
        List<Double> sorted = values.stream().sorted().toList();

        for (int i = 0; i < STATISTICS.size(); i++) {
            item.add(season + STATISTICS.get(i), quantile(sorted, QUANTILES[i]));
        }
    }

    private double quantile(List<Double> sorted, double p) {
        double index = p * (sorted.size() - 1);
        int lower = (int) Math.floor(index);
        int upper = (int) Math.ceil(index);

        return sorted.get(lower) + (sorted.get(upper) - sorted.get(lower)) * (index - lower);
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




Month.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.jspecify.annotations.Nullable;

public enum Month implements EnumClass<String> {

    JANUARY("january"),
    FEBRUARY("february"),
    MARCH("march"),
    APRIL("april"),
    MAY("may"),
    JUNE("june"),
    JULY("july"),
    AUGUST("august"),
    SEPTEMBER("september"),
    OCTOBER("october"),
    NOVEMBER("november"),
    DECEMBER("december");

    private final String id;

    Month(String id) {
        this.id = id;
    }

    @Override
    public String getId() {
        return id;
    }

    @Nullable
    public static Month fromId(String id) {
        for (Month at : Month.values()) {
            if (at.getId().equals(id)) {
                return at;
            }
        }
        return null;
    }
}


