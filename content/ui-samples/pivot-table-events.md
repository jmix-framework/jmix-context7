<Path>Add-ons > PivotTable > PivotTable events</Path>

PivotTable supports two component-specific types of events. The PivotTableRefreshEvent event is fired when the component parameters are changed via UI elements. The PivotTableCellClickEvent event fires when a table cell is clicked. This event returns all entities whose attributes were used in the aggregation in that cell.

pivot-table-events.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:pvttbl="http://jmix.io/schema/pvttbl/ui">
    <data>
        <collection id="temperatureDataDc"
                    class="io.jmix.uisamples.entity.TemperatureData">
            <fetchPlan extends="_local"/>
            <loader id="tipsLoader">
                <query>
                    <![CDATA[select e from TemperatureData e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <pvttbl:pivotTable id="pivotTable"
                           dataContainer="temperatureDataDc"
                           showColumnTotals="false"
                           showRowTotals="false"
                           showUI="true">
            <pvttbl:properties>
                <pvttbl:property name="temperature"/>
                <pvttbl:property name="city"/>
                <pvttbl:property name="month"/>
            </pvttbl:properties>
            <pvttbl:columns>
                <pvttbl:column value="month"/>
            </pvttbl:columns>
            <pvttbl:rows>
                <pvttbl:row value="city"/>
            </pvttbl:rows>
            <pvttbl:aggregations selected="AVERAGE">
                <pvttbl:aggregation mode="AVERAGE"/>
                <pvttbl:aggregation mode="COUNT"/>
                <pvttbl:aggregation mode="MAXIMUM"/>
            </pvttbl:aggregations>
            <pvttbl:aggregationProperties>
                <pvttbl:property name="temperature"/>
            </pvttbl:aggregationProperties>
        </pvttbl:pivotTable>
    </layout>
</view>



PivotTableEvents.java

package io.jmix.uisamples.view.flowui.pivottable.events;

import io.jmix.core.Messages;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.*;
import io.jmix.pivottableflowui.component.PivotTable;
import io.jmix.pivottableflowui.kit.component.model.AggregationMode;
import io.jmix.pivottableflowui.kit.component.model.Renderer;
import io.jmix.pivottableflowui.kit.event.PivotTableCellClickEvent;
import io.jmix.pivottableflowui.kit.event.PivotTableRefreshEvent;
import io.jmix.pivottableflowui.kit.event.PivotTableRefreshEventDetail;
import io.jmix.uisamples.entity.TemperatureData;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;
import java.util.stream.Collectors;

@ViewController("pivot-table-events")
@ViewDescriptor("pivot-table-events.xml")
public class PivotTableEvents extends StandardView {

    @ViewComponent
    private PivotTable<TemperatureData> pivotTable;

    @Autowired
    private Notifications notifications;
    @Autowired
    private Messages messages;

    @Subscribe("pivotTable")
    public void onPivotTablePivotTableCellClick(final PivotTableCellClickEvent<?> event) {
        List<TemperatureData> items = event.getDetail().getItems();

        String message = items.stream()
                .map(temperatureData -> "Entity id: %s, Celsius: %d".formatted(
                                temperatureData.getId(), temperatureData.getTemperature()
                        )
                )
                .collect(Collectors.joining("\n"));

        notifications.show("Cell click event (items in the cell)", message);
    }

    @Subscribe("pivotTable")
    public void onPivotTablePivotTableRefresh(final PivotTableRefreshEvent event) {
        PivotTableRefreshEventDetail refreshDetail = event.getDetail();
        String message = """
                Renderer: %s
                Aggregation: %s
                Rows: %s
                Columns: %s
                """.formatted(
                getRendererMessage(refreshDetail.getRenderer()),
                getAggregatorMessage(refreshDetail.getAggregationMode()),
                getLocalizedProperties(refreshDetail.getRows()),
                getLocalizedProperties(refreshDetail.getColumns())
        );

        notifications.show("Refresh event", message);
    }

    private String getRendererMessage(Renderer renderer) {
        return messages.getMessage("pivottable.renderer." + renderer.getId());
    }

    private String getAggregatorMessage(AggregationMode aggregationMode) {
        return messages.getMessage("pivottable.aggregator." + aggregationMode.getId());
    }

    private String getLocalizedProperties(List<String> properties) {
        if (CollectionUtils.isEmpty(properties)) {
            return "[Empty]";
        }

        return properties.stream()
                .map(pivotTable.getProperties()::get)
                .collect(Collectors.joining(", "));
    }
}




TipInfo.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.springframework.lang.Nullable;

import java.math.BigDecimal;
import java.util.UUID;

@Table(name = "TIP_INFO")
@Entity
@JmixEntity
public class TipInfo {

    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    @Id
    private UUID id;

    @Column(name = "TOTAL_BILL", nullable = false, precision = 19, scale = 2)
    private BigDecimal totalBill;

    @Column(name = "TIP", nullable = false, precision = 19, scale = 2)
    private BigDecimal tip;

    @Column(name = "SMOKER", nullable = false)
    private Boolean smoker = false;

    @Column(name = "SIZE_", nullable = false)
    private Integer size;

    @Column(name = "SEX")
    private String sex;

    @Column(name = "DAY_")
    private String day;

    @Column(name = "TIME_")
    private String time;

    @Nullable
    public Time getTime() {
        return time == null ? null : Time.fromId(time);
    }

    public void setTime(@Nullable Time time) {
        this.time = time == null ? null : time.getId();
    }

    @Nullable
    public Day getDay() {
        return day == null ? null : Day.fromId(day);
    }

    public void setDay(@Nullable Day day) {
        this.day = day == null ? null : day.getId();
    }

    @Nullable
    public Sex getSex() {
        return sex == null ? null : Sex.fromId(sex);
    }

    public void setSex(@Nullable Sex sex) {
        this.sex = sex == null ? null : sex.getId();
    }

    public Integer getSize() {
        return size;
    }

    public void setSize(Integer size) {
        this.size = size;
    }

    public Boolean getSmoker() {
        return smoker;
    }

    public void setSmoker(Boolean smoker) {
        this.smoker = smoker;
    }

    public BigDecimal getTip() {
        return tip;
    }

    public void setTip(BigDecimal tip) {
        this.tip = tip;
    }

    public BigDecimal getTotalBill() {
        return totalBill;
    }

    public void setTotalBill(BigDecimal totalBill) {
        this.totalBill = totalBill;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}


