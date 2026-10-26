<Path>Add-ons > Charts > Series > Bar series > Waterfall Bar series</Path>

A waterfall chart shows how a total breaks down into parts. It is built from two `bar` series in the same `stack`.

The first series is an invisible placeholder: its `itemStyle` sets a transparent `color` and `borderColor`, and `silent` turns off its reaction to the mouse. The placeholder lifts each visible bar to the amount that remains after the previous expenses. The controller calculates these heights when it fills the data set.

The tooltip `formatterFunction` shows only the visible series.


bar-series-waterfall.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Monthly expenses" left="0" top="0"/>
            <charts:tooltip trigger="AXIS">
                <charts:formatterFunction>
                    <![CDATA[
                        function (params) {
                            var expense = params[1];

                            return expense.name + ': ' + expense.value.amount;
                        }
                    ]]>
                </charts:formatterFunction>
                <charts:axisPointer type="SHADOW"/>
            </charts:tooltip>

            <charts:xAxes>
                <charts:xAxis type="CATEGORY"/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis/>
            </charts:yAxes>

            <charts:series>
                <charts:bar name="Placeholder" stack="total" silent="true">
                    <charts:itemStyle color="transparent" borderColor="transparent"/>
                </charts:bar>
                <charts:bar name="Amount" stack="total">
                    <charts:label show="true" position="INSIDE"/>
                </charts:bar>
            </charts:series>
        </charts:chart>
    </layout>
</view>




BarSeriesWaterfallSample.java

package io.jmix.uisamples.view.flowui.charts.series.bar.waterfall;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.util.List;
import java.util.Map;

@ViewController("bar-series-waterfall")
@ViewDescriptor("bar-series-waterfall.xml")
public class BarSeriesWaterfallSample extends StandardView {

    @ViewComponent
    private Chart chart;

    @Subscribe
    public void onInit(InitEvent event) {
        List<Map.Entry<String, Integer>> expenses = List.of(
                Map.entry("Rent", 1200),
                Map.entry("Utilities", 300),
                Map.entry("Transportation", 200),
                Map.entry("Meals", 900),
                Map.entry("Other", 300)
        );

        int rest = expenses.stream()
                .mapToInt(Map.Entry::getValue)
                .sum();
        ListChartItems<MapDataItem> items = new ListChartItems<>(createItem("Total", 0, rest));

        for (Map.Entry<String, Integer> expense : expenses) {
            rest -= expense.getValue();
            items.addItem(createItem(expense.getKey(), rest, expense.getValue()));
        }

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(items)
                                        .withCategoryField("category")
                                        .withValueFields("placeholder", "amount")
                        )
        );
    }

    protected MapDataItem createItem(String category, int placeholder, int amount) {
        return new MapDataItem(Map.of("category", category,
                "placeholder", placeholder,
                "amount", amount));
    }
}


