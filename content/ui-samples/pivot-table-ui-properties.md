<Path>Add-ons > PivotTable > PivotTable UI properties</Path>

PivotTable has a special mode that displays UI elements for data manipulation. The showUI attribute is responsible for this functionality. If PivotTable is disabled with method PivotTable#setEnabled(false) call, its UI controls are also disabled. The following attributes can be applied on any mode, but only for the table renderers: showRowTotals shows and hides row totals; showColTotals shows and hides column totals.

pivot-table-ui-properties.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:pvttbl="http://jmix.io/schema/pvttbl/ui">
    <data>
        <collection id="tipsDc"
                    class="io.jmix.uisamples.entity.TipInfo">
            <fetchPlan extends="_local"/>
            <loader id="tipsLoader">
                <query>
                    <![CDATA[select e from TipInfo e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox classNames="buttons-panel">
            <checkbox id="showRowTotalsCheckbox" label="msg://showRowTotalsCheckbox.label" value="true"/>
            <checkbox id="showColumnTotalsCheckbox" label="msg://showColumnTotalsCheckbox.label" value="true"/>
            <checkbox id="showUiCheckbox" label="msg://showUiCheckbox.label" value="true"/>
            <checkbox id="disableCheckbox" label="msg://disableCheckbox.label" value="false"/>
        </hbox>
        <pvttbl:pivotTable id="pivotTable"
                           dataContainer="tipsDc"
                           showColumnTotals="true"
                           showRowTotals="true"
                           showUI="true">
            <pvttbl:properties>
                <pvttbl:property name="totalBill"/>
                <pvttbl:property name="tip"/>
                <pvttbl:property name="sex"/>
                <pvttbl:property name="smoker"/>
                <pvttbl:property name="day"/>
                <pvttbl:property name="time"/>
                <pvttbl:property name="size"/>
            </pvttbl:properties>
            <pvttbl:columns>
                <pvttbl:column value="day"/>
                <pvttbl:column value="time"/>
            </pvttbl:columns>
            <pvttbl:rows>
                <pvttbl:row value="sex"/>
                <pvttbl:row value="smoker"/>
            </pvttbl:rows>
        </pvttbl:pivotTable>
    </layout>
</view>



PivotTableUiProperties.java

package io.jmix.uisamples.view.flowui.pivottable.uiproperties;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.view.*;
import io.jmix.pivottableflowui.component.PivotTable;
import io.jmix.uisamples.entity.TipInfo;

@ViewController("pivot-table-ui-properties")
@ViewDescriptor("pivot-table-ui-properties.xml")
public class PivotTableUiProperties extends StandardView {

    @ViewComponent
    private PivotTable<TipInfo> pivotTable;

    @Subscribe(id = "showRowTotalsCheckbox", subject = "clickListener")
    public void onShowRowTotalsCheckboxClick(final ClickEvent<JmixCheckbox> event) {
        pivotTable.setShowRowTotals(event.getSource().getValue());
    }

    @Subscribe(id = "showColumnTotalsCheckbox", subject = "clickListener")
    public void onShowColumnTotalsCheckboxClick(final ClickEvent<JmixCheckbox> event) {
        pivotTable.setShowColumnTotals(event.getSource().getValue());
    }

    @Subscribe(id = "showUiCheckbox", subject = "clickListener")
    public void onShowUiCheckboxClick(final ClickEvent<JmixCheckbox> event) {
        pivotTable.setShowUI(event.getSource().getValue());
    }

    @Subscribe(id = "disableCheckbox", subject = "clickListener")
    public void onDisableCheckboxClick(final ClickEvent<JmixCheckbox> event) {
        pivotTable.setEnabled(!event.getSource().getValue());
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


