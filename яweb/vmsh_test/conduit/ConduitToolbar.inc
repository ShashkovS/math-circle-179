<?php

if (!defined('IN_CONDUIT')){
    // Попытка прямого доступа к файлу
    exit();
}

?>
        <section class="bar toolbar">
            <ul>
                <li class="hide">
                    <span>&#9650;&nbsp;Свернуть</span>
                </li>
                <li class="tool">
                    <dl>
                        <dt><label for="classSelector">Класс:</label></dt>
                        <dd>
                            <select id="classSelector">
                                <?php fillClassSelector($ClassID); ?>
                            </select>
                        </dd>
                        <dt><label for="listSelector">Листок:</label></dt>
                        <dd>
                            <select id="listSelector">
                                <?php fillListSelector($ListID, $ClassID); ?>
                            </select>
                        </dd>
                    </dl>
                </li>
                <li class="tool">
                    <ul>
                        <li>
                            <input id="HM_CB" type="checkbox" />
                            <label for="HM_CB">Подсветить текущие метки</label>
                        </li>
                        <li>
                            <label for="autoCaption">Метка:</label>
                            <input id="autoCaption" type="text" maxlength=10 />
                        </li>
                    </ul>
                </li>
                <li class="tool">
                    <button id="undoButton" type="button" title="Отмена последнего действия">Отменить</button>
                </li>
            </ul>
        </section>
