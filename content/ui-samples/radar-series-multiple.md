<Path>Add-ons > Charts > Series > Radar series > Multiple Radar series</Path>

RadarSeries also supports multiple objects.

radar-series-multiple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:radar>
                <charts:indicators>
                    <charts:indicator name="Sales" max="6500"/>
                    <charts:indicator name="Administration" max="16000"/>
                    <charts:indicator name="Information Technology" max="30000"/>
                    <charts:indicator name="Customer Support" max="38000"/>
                    <charts:indicator name="Development" max="52000"/>
                    <charts:indicator name="Marketing" max="25000"/>
                </charts:indicators>
            </charts:radar>

            <charts:series>
                <charts:radar/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




RadarSeriesMultipleSample.java

package io.jmix.uisamples.view.flowui.charts.series.radar.multiple;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.util.Map;

@ViewController("radar-series-multiple")
@ViewDescriptor("radar-series-multiple.xml")
public class RadarSeriesMultipleSample extends StandardView {

    @ViewComponent
    protected Chart chart;

    @Subscribe
    protected void onInit(InitEvent event) {
        ListChartItems<MapDataItem> items = new ListChartItems<>(
                new MapDataItem(
                        Map.of(
                                "Sales", 4200,
                                "Administration", 3000,
                                "Information Technology", 20000,
                                "Customer Support", 35000,
                                "Development", 50000,
                                "Marketing", 18000
                        )
                ),
                new MapDataItem(
                        Map.of(
                                "Sales", 5000,
                                "Administration", 14000,
                                "Information Technology", 28000,
                                "Customer Support", 26000,
                                "Development", 42000,
                                "Marketing", 21000
                        )
                )
        );

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(items)
                                        .withValueFields(
                                                "Sales",
                                                "Administration",
                                                "Information Technology",
                                                "Customer Support",
                                                "Development",
                                                "Marketing"
                                        )
                        )
        );
    }
}


