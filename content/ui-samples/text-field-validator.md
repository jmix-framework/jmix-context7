<Path>Components > TextField > TextField with Validator</Path>

Text field can be assigned a validator - a class implementing Validator interface. The validator limits user input in addition to what is already done by the datatype.

text-field-validator.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <textField id="integerTextField" label="Positive TextField"
                   helperText="Value must be positive"
                   datatype="int">
            <validators>
                <custom bean="uisamples_PositiveIntegerValidator"/>
            </validators>
        </textField>
        <textField id="doubleTextField" label="Double range validator"
                   helperText="Value must be between 1.0 and 100.0"
                   datatype="double">
            <validators>
                <doubleMin value="1.0" inclusive="true"/>
                <doubleMax value="100.0" inclusive="true"/>
            </validators>
        </textField>
    </layout>
</view>




TextFieldValidatorSample.java

package io.jmix.uisamples.view.flowui.components.textfield.validator;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("text-field-validator")
@ViewDescriptor("text-field-validator.xml")
public class TextFieldValidatorSample extends StandardView {
}




PositiveIntegerValidator.java

package io.jmix.uisamples.bean;

import io.jmix.core.common.util.ParamsMap;
import io.jmix.flowui.component.validation.AbstractValidator;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component("uisamples_PositiveIntegerValidator")
@Scope(BeanDefinition.SCOPE_PROTOTYPE)
public class PositiveIntegerValidator extends AbstractValidator<Integer> {

    @Override
    public void accept(Integer value) {
        if (value != null) {
            if (value <= 0) {
                fireValidationException(
                        messages.getMessage("validation.constraints.positive"),
                        ParamsMap.of("value", value)
                );
            }
        }
    }
}


