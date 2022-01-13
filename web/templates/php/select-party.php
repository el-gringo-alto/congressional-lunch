<?php if (strtolower($_GET['header']) != 'false'): ?>
    <section id="party-select" aria-label="Party filtering">
        <label for="party">Party to view</label>
        <select name="party" id="party">
            <option value="both" <?php
                if (strtolower($_GET['party']) != 'democratic' &&
                    strtolower($_GET['party']) != 'republican') {
                    echo 'selected';
                }
            ?>>Both</option>
            <option value="democratic" <?php
                if (strtolower($_GET['party']) == 'democratic') {
                    echo 'selected';
                }
            ?>>Democratic</option>
            <option value="republican" <?php
                if (strtolower($_GET['party']) == 'republican') {
                    echo 'selected';
                }
            ?>>Republican</option>
        </select>

        <script>
            var partySelectBox = document.getElementById('party');

            document.getElementById('party').addEventListener('change', () => {
                party = partySelectBox.options[partySelectBox.selectedIndex].value;
                getTweetStream();
            })

        </script>

    </section>
<?php endif; ?>
