<Path>Add-ons > Charts > Series > Pie series > Donut series</Path>

DonutSeries is just a simple PieSereis with a hole inside. You can define hole radius to any size you need, both in percent or pixels using radius attribute.

donut-series.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Donut chart"/>
            <charts:legend top="0"/>
            <charts:tooltip trigger="ITEM" formatter="{b}: {d}%"/>

            <charts:series>
                <charts:pie name="Category" radius="50% 80%">
                    <charts:label show="false" position="CENTER"/>
                    <charts:labelLine show="false"/>
                    <charts:emphasis>
                        <charts:label show="true" fontSize="40" fontWeight="bold"/>
                    </charts:emphasis>
                </charts:pie>
            </charts:series>
        </charts:chart>
    </layout>
</view>




DonutSeriesSample.java

package io.jmix.uisamples.view.flowui.charts.series.pie.donut;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.util.Map;

@ViewController("donut-series")
@ViewDescriptor("donut-series.xml")
public class DonutSeriesSample extends StandardView {

    @ViewComponent
    protected Chart chart;

    @Subscribe
    protected void onInit(InitEvent event) {
        ListChartItems<MapDataItem> items = new ListChartItems<>(
                new MapDataItem(Map.of("category", "New", "value", 4852)),
                new MapDataItem(Map.of("category", "Returning", "value", 9899))
        );

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(items)
                                        .withCategoryField("category")
                                        .withValueField("value")
                        )
        );
    }
}


