<Path>Components > DataGrid > DataGrid with popover renderer</Path>

`popoverRenderer` suits columns with long text values. It shows the value as clickable text, which is cut with an ellipsis if it does not fit into the cell. A click on the value opens a popover with the full text.

The `position` attribute sets where the popover opens, `BOTTOM_START` by default.


data-grid-popover-renderer.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="contractsDc"
                    class="io.jmix.uisamples.entity.Contract">
            <fetchPlan extends="_base">
                <property name="customer" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="contractsDl">
                <query>
                    <![CDATA[select e from Contract e order by e.number]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <dataGrid id="contractsDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="contractsDc">
            <columns>
                <column property="number"/>
                <column property="date"/>
                <column property="customer"/>
                <column property="status"/>
                <column property="comments">
                    <popoverRenderer/>
                </column>
            </columns>
        </dataGrid>
    </layout>
</view>




DataGridPopoverRendererSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.popoverrenderer;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("data-grid-popover-renderer")
@ViewDescriptor("data-grid-popover-renderer.xml")
public class DataGridPopoverRendererSample extends StandardView {
}




Contract.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.UUID;

@JmixEntity
@Table(name = "CONTRACT", indexes = {
        @Index(name = "IDX_CONTRACT_CUSTOMER", columnList = "CUSTOMER_ID")
})
@Entity
public class Contract {
    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @Column(name = "DATE_")
    private LocalDate date;

    @Column(name = "NUMBER_")
    private String number;

    @InstanceName
    @Column(name = "DESCRIPTION")
    private String description;

    @JoinColumn(name = "CUSTOMER_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private Customer customer;

    @Column(name = "STATUS", length = 1)
    private String status;

    @Column(name = "COMMENTS")
    @Lob
    private String comments;

    public String getComments() {
        return comments;
    }

    public void setComments(String comments) {
        this.comments = comments;
    }

    public ContractStatus getStatus() {
        return status == null ? null : ContractStatus.fromId(status);
    }

    public void setStatus(ContractStatus status) {
        this.status = status == null ? null : status.getId();
    }

    public Customer getCustomer() {
        return customer;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

}

