<Path>Add-ons > Charts > Series > Boxplot series > Simple Boxplot series</Path>

A boxplot shows how values are spread. The box spans from the first quartile to the third one, the line inside the box marks the median, and the whiskers reach the minimum and the maximum.

The `boxplot` series takes five values for each category. `encode` lists them for the value axis in this order: `y="min, q1, median, q3, max"`, and `x` sets the category field. The same list in `tooltip` makes the tooltip show all five values.

The chart doesn't calculate these values from raw data, so the data set must already contain them. See how to calculate them in the controller in the [Multiple Boxplot series]({contextPath}/sample/boxplot-series-multiple) sample.


boxplot-series-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Delivery time" subtext="Days, by regions" left="0" top="0"/>
            <charts:tooltip trigger="ITEM"/>

            <charts:xAxes>
                <charts:xAxis type="CATEGORY"/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis/>
            </charts:yAxes>

            <charts:series>
                <charts:boxplot name="Delivery time">
                    <charts:encode x="region" y="min, q1, median, q3, max"
                                   tooltip="min, q1, median, q3, max"/>
                </charts:boxplot>
            </charts:series>
        </charts:chart>
    </layout>
</view>




BoxplotSeriesSimpleSample.java

package io.jmix.uisamples.view.flowui.charts.series.boxplot.simple;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.util.Map;

@ViewController("boxplot-series-simple")
@ViewDescriptor("boxplot-series-simple.xml")
public class BoxplotSeriesSimpleSample extends StandardView {

    @ViewComponent
    private Chart chart;

    @Subscribe
    public void onInit(InitEvent event) {
        ListChartItems<MapDataItem> items = new ListChartItems<>(
                createItem("North", 1, 2, 3, 4, 7),
                createItem("South", 2, 3, 4, 6, 9),
                createItem("East", 1, 2, 2.5, 3.5, 5),
                createItem("West", 2, 4, 5, 6, 10),
                createItem("Central", 1, 1.5, 2, 3, 4)
        );

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(items)
                                        .withCategoryField("region")
                                        .withValueFields("min", "q1", "median", "q3", "max")
                        )
        );
    }

    private MapDataItem createItem(String region, double min, double q1, double median, double q3, double max) {
        return new MapDataItem(Map.of("region", region,
                "min", min,
                "q1", q1,
                "median", median,
                "q3", q3,
                "max", max));
    }
}


